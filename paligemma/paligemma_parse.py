"""Parses PaliGemma output."""
"""Taken from https://huggingface.co/spaces/big-vision/paligemma/tree/main"""

import functools
import re

import flax.linen as nn
import jax
import jax.numpy as jnp
import numpy as np
import PIL.Image


EXAMPLE_STRING = '<loc0000><loc0000><loc0930><loc1012> <seg114><seg074><seg106><seg044><seg030><seg027><seg119><seg119><seg120><seg117><seg082><seg082><seg051><seg005><seg125><seg097> wall ; <loc0722><loc0047><loc0895><loc0378> <seg068><seg114><seg014><seg037><seg029><seg063><seg048><seg104><seg010><seg056><seg021><seg056><seg019><seg017><seg102><seg121> car ; <loc0180><loc0596><loc0782><loc0961> <seg026><seg028><seg028><seg026><seg104><seg026><seg029><seg022><seg000><seg068><seg092><seg125><seg003><seg127><seg121><seg043> david bowie ; <loc0234><loc0043><loc0736><loc0289> <seg068><seg008><seg091><seg064><seg007><seg055><seg017><seg090><seg042><seg052><seg068><seg086><seg001><seg014><seg093><seg052> david bowie ; <loc0230><loc0300><loc0736><loc0499> <seg073><seg011><seg114><seg059><seg048><seg097><seg091><seg022><seg007><seg036><seg091><seg022><seg016><seg009><seg003><seg036> david bowie'  # pylint: disable=line-too-long

_MODEL_PATH = 'paligemma/vae-oid.npz'

_SEGMENT_DETECT_RE = re.compile(
    r'(.*?)' +
    r'<loc(\d{4})>' * 4 + r'\s*' +
    '(?:%s)?' % (r'<seg(\d{3})>' * 16) +
    r'\s*([^;<>]+)? ?(?:; )?',
)


def _get_params(checkpoint):
  """Converts PyTorch checkpoint to Flax params."""

  def transp(kernel):
    return np.transpose(kernel, (2, 3, 1, 0))

  def conv(name):
    return {
        'bias': checkpoint[name + '.bias'],
        'kernel': transp(checkpoint[name + '.weight']),
    }

  def resblock(name):
    return {
        'Conv_0': conv(name + '.0'),
        'Conv_1': conv(name + '.2'),
        'Conv_2': conv(name + '.4'),
    }

  return {
      '_embeddings': checkpoint['_vq_vae._embedding'],
      'Conv_0': conv('decoder.0'),
      'ResBlock_0': resblock('decoder.2.net'),
      'ResBlock_1': resblock('decoder.3.net'),
      'ConvTranspose_0': conv('decoder.4'),
      'ConvTranspose_1': conv('decoder.6'),
      'ConvTranspose_2': conv('decoder.8'),
      'ConvTranspose_3': conv('decoder.10'),
      'Conv_1': conv('decoder.12'),
  }


def _quantized_values_from_codebook_indices(codebook_indices, embeddings):
  batch_size, num_tokens = codebook_indices.shape
  assert num_tokens == 16, codebook_indices.shape
  unused_num_embeddings, embedding_dim = embeddings.shape

  encodings = jnp.take(embeddings, codebook_indices.reshape((-1)), axis=0)
  encodings = encodings.reshape((batch_size, 4, 4, embedding_dim))
  return encodings


@functools.cache
def _get_reconstruct_masks():
  """Reconstructs masks from codebook indices.

  Returns:
    A function that expects indices shaped `[B, 16]` of dtype int32, each
    ranging from 0 to 127 (inclusive), and that returns a decoded masks sized
    `[B, 64, 64, 1]`, of dtype float32, in range [-1, 1].
  """

  class ResBlock(nn.Module):
    features: int

    @nn.compact
    def __call__(self, x):
      original_x = x
      x = nn.Conv(features=self.features, kernel_size=(3, 3), padding=1)(x)
      x = nn.relu(x)
      x = nn.Conv(features=self.features, kernel_size=(3, 3), padding=1)(x)
      x = nn.relu(x)
      x = nn.Conv(features=self.features, kernel_size=(1, 1), padding=0)(x)
      return x + original_x

  class Decoder(nn.Module):
    """Upscales quantized vectors to mask."""

    @nn.compact
    def __call__(self, x):
      num_res_blocks = 2
      dim = 128
      num_upsample_layers = 4

      x = nn.Conv(features=dim, kernel_size=(1, 1), padding=0)(x)
      x = nn.relu(x)

      for _ in range(num_res_blocks):
        x = ResBlock(features=dim)(x)

      for _ in range(num_upsample_layers):
        x = nn.ConvTranspose(
            features=dim,
            kernel_size=(4, 4),
            strides=(2, 2),
            padding=2,
            transpose_kernel=True,
        )(x)
        x = nn.relu(x)
        dim //= 2

      x = nn.Conv(features=1, kernel_size=(1, 1), padding=0)(x)

      return x

  def reconstruct_masks(codebook_indices):
    quantized = _quantized_values_from_codebook_indices(
        codebook_indices, params['_embeddings']
    )
    return Decoder().apply({'params': params}, quantized)

  with open(_MODEL_PATH, 'rb') as f:
    params = _get_params(dict(np.load(f)))

  return jax.jit(reconstruct_masks, backend='cpu')


def extract_objs(text, width, height, unique_labels=False):
  """Returns objs for a string with "<loc>" and "<seg>" tokens."""
  objs = []
  seen = set()
  while text:
    m = _SEGMENT_DETECT_RE.match(text)
    if not m:
      break

    gs = list(m.groups())
    before = gs.pop(0)
    name = gs.pop()
    y1, x1, y2, x2 = [int(x) / 1024 for x in gs[:4]]
    y1, x1, y2, x2 = map(round, (y1*height, x1*width, y2*height, x2*width))

    seg_indices = gs[4:20]
    if seg_indices[0] is None:
      mask = None
    else:
      seg_indices = np.array([int(x) for x in seg_indices], dtype=np.int32)
      m64, = _get_reconstruct_masks()(seg_indices[None])[..., 0]
      m64 = np.clip(np.array(m64) * 0.5 + 0.5, 0, 1)
      m64 = PIL.Image.fromarray((m64 * 255).astype('uint8'))
      mask = np.zeros([height, width])
      if y2 > y1 and x2 > x1:
        mask[y1:y2, x1:x2] = np.array(m64.resize([x2 - x1, y2 - y1])) / 255.0

    content = m.group()
    if before:
      objs.append(dict(content=before))
      content = content[len(before):]
    while unique_labels and name in seen:
      name = (name or '') + "'"
    seen.add(name)
    objs.append(dict(
        content=content, xyxy=(x1, y1, x2, y2), mask=mask, name=name))
    text = text[len(before) + len(content):]

  if text:
    objs.append(dict(content=text))

  return objs


if __name__ == '__main__':
  # Simple test.
  print([
      {
          k: (v.shape, v.mean()) if isinstance(v, np.ndarray) else v
          for k, v in obj.items()
      }
      for obj in extract_objs(EXAMPLE_STRING, 100, 200)
  ])
