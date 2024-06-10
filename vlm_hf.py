from typing import Tuple
from vlm import VLM
from config import Config
from PIL import Image
from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor
import paligemma.paligemma_parse as paligemma_parse
from PIL import ImageDraw

class VLM_HF(VLM):
    debug = False

    def __init__(self):
        general_config = Config()
        vlm_config = general_config.get_vlm_config()
        self.model = PaliGemmaForConditionalGeneration.from_pretrained(vlm_config["model"]).to("cuda")
        self.processor = PaliGemmaProcessor.from_pretrained(vlm_config["model"])

    def patch_size(self) -> Tuple[int, int]:
        """
        Get the native image patch size
        """
        return (448, 448)

    def desc_en(self, image: Image) -> str:
        """
            Describe image in English language
        """
        return self._run_pali(image, "Describe the image including any text")

    def check_patch_for_button(self, patch: Image, button: str) -> str:
        if button == "options":
            return self._find_options(patch)

    def _find_options(self, patch: Image):
        opts_present = self._run_pali(patch, f"Is there a share button?")
        if opts_present == "yes":
            seg = self._run_pali(patch, "segment share")
            if seg and seg != "<eos>":
                width, height = patch.size
                objs = paligemma_parse.extract_objs(seg, width, height, unique_labels=True)

                # Reject objects that touch on the border of the attention window (may be truncated)
                objs = [obj for obj in objs if 'xyxy' in obj and not (obj['xyxy'][0] == 0 or obj['xyxy'][1] == 0 or obj['xyxy'][2] == 448 or obj['xyxy'][3] == 448)]

                # Compile bounding boxes
                ret = [obj['xyxy'] for obj in objs]

                if self.debug:
                    self._dump_seg(patch, objs)

                return ret
        return None

    def _dump_seg(self, patch: Image, objs):
        patch.save("/tmp/seg-org.png")

        draw = ImageDraw.Draw(patch, "RGBA")  # Use RGBA to allow for alpha blending

        # Create an RGBA version of the mask with varying color hue based on confidence
        mask_image = Image.new("RGBA", patch.size)
        mask_draw = ImageDraw.Draw(mask_image)

        for obj in objs:
            mask = obj['mask']
            if mask is not None:
                # Apply the mask to the image using a color map that reflects confidence
                for y in range(mask.shape[0]):
                    for x in range(mask.shape[1]):
                        # Assuming mask values are between 0 and 1, scale to 255
                        confidence = int(mask[y, x] * 255)
                        # Set a blue color with varying opacity based on the mask's confidence value
                        conf = mask[y, x]
                        if conf < 0.5:
                            color = (0, 0, 255, confidence)
                        elif conf > 0.95:
                            color = (255, 0, 0, confidence)
                        elif conf > 0.7:
                            color = (0, 255, 0, confidence)
                        elif conf >= 0.5:
                            color = (0, 0, 0, confidence)
                        mask_draw.point((x, y), color)

            # Draw the bounding box
            x1, y1, x2, y2 = obj['xyxy']
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # Composite the mask image with the original patch
        patch = Image.alpha_composite(patch.convert("RGBA"), mask_image)

        patch.save("/tmp/seg-mask.png")

    def _run_pali(self, img: Image, prompt: str) -> str:
        inputs = self.processor(images=img, text=prompt, return_tensors="pt").to("cuda")

        predictions = self.model.generate(**inputs, max_new_tokens=100)
        pali_ret = self.processor.decode(predictions[0], skip_special_tokens=True)[len(prompt):].lstrip("\n")
        return pali_ret
