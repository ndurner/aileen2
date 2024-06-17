from singleton_decorator import singleton
from PIL import Image, ImageDraw
import os
from typing import Tuple, List
import numpy as np
import re

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "vlm.npz")

TOKENIZER_DIR = "tokenizer"
TOKENIZER_PATH = os.path.join(TOKENIZER_DIR, "vlm_tokenizer.model")

class VLM:
    """Visual model implementation"""

    def patch_size(self) -> Tuple[int, int]:
        """
        Get the native image patch size
        """
        pass

    def desc_en(self, image: Image) -> str:
        """
            Describe image in English language
        """
        pass

    def scan_for_button(self, image: Image, button: str) -> List[Tuple[int, int, int, int]]:
        """
        Searches for a button that the model recognizes as 'button'.
        Accumulates results from patches where the button is found.
        """
        results = self._iterate_through_patches(image, self.check_patch_for_button, button=button, terminate_on_find=True)

        return results
    
    def check_patch_for_button(self, patch: Image, button: str) -> str:
        """
        Return button in PaliGemma segment format if found
        """
        pass

    def question(self, question: str) -> str:
        """
        Answer a question on the image
        """
        pass

    def _iterate_through_patches(self, image, process_patch, terminate_on_find=False, **kwargs):
        patch_size = self.patch_size()[0]  # Assuming square patches
        stride = patch_size // 2

        width, height = image.size
        ret = []
        patch_idx = 0
        for y in range(0, height - patch_size + 1, stride):
            for x in range(0, width - patch_size + 1, stride):
                patch = image.crop((x, y, x + patch_size, y + patch_size))
                if self.debug:
                    patch.save(f"/tmp/crop-{x}-{y}-{patch_idx}.png")
                    patch_idx = patch_idx + 1
                results = process_patch(patch, **kwargs)
                if results:
                    for i, result in enumerate(results):
                        # make patch-local coords image-global
                        results[i] = (result[0] + x, result[1] + y, result[2] + x, result[3] + y)

                    ret.extend(results)

                    if terminate_on_find:
                        return ret

        return ret
