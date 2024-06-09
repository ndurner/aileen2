from singleton_decorator import singleton
from PIL import Image
import os
from typing import Tuple

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

    def scan_for_button(self, image: Image, button: str) -> Tuple[int, int, int, int]:
        """
        Searches for a button that the model recognizes as 'button'.
        Returns button location
        """
        
        self._iterate_through_patches(self, image, lambda patch: self.check_patch_for_button(self, patch, button))

    def check_patch_for_button(self, patch: Image, button: str) -> str:
        """
        Return button in PaliGemma segment format if found
        """
        pass

    def _iterate_through_patches(self, image: Image, process_patch):
        """
        Iterates through the image in overlapping 448x448 patches.
        
        :param image: A PIL Image object representing the image.
        :param process_patch: A function to process each patch.
        """
        patch_size = 448
        stride = 224
        ret = []

        width, height = image.size
        for y in range(0, height - patch_size + 1, stride):
            for x in range(0, width - patch_size + 1, stride):
                patch = image.crop((x, y, x + patch_size, y + patch_size))
                ret.append(process_patch(patch))
