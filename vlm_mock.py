from singleton_decorator import singleton
from PIL import Image
import os
from vlm import VLM
from typing import Tuple, List

# Configuration
dump_images = False

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "vlm.npz")

TOKENIZER_DIR = "tokenizer"
TOKENIZER_PATH = os.path.join(TOKENIZER_DIR, "vlm_tokenizer.model")

class VLM_Mock(VLM):
    """Visual model implementation"""

    desc_calls = 0

    def patch_size(self) -> Tuple[int, int]:
        """
        Get the native image patch size
        """
        return (448, 448)

    def desc_en(self, image: Image) -> str:
        """
            Describe image in English language
        """
        
        if dump_images:
            image.save("/tmp/desc_en.jpg")

        if self.desc_calls == 0:
            ret = "a website with videos and a play button"
    #        ret = "error page"
        else:
            ret = "a screen shot of a website for the mediathek."

        self.desc_calls = self.desc_calls + 1

        return ret

    def question(self, question: str) -> str:
        """
        Answer a question on the image
        """
        if question == "Is there a 'Untertitel' button?":
            return "yes"
        else:
            return "unanswerable"

    def scan_for_button(self, image: Image, button: str) -> List[Tuple[int, int, int, int]]:
        """
        Searches for a button that the model recognizes as 'button'.
        Returns button location
        """

        self.patch_idx = 0
        self._iterate_through_patches(image, lambda patch: self.save_patches(patch))

        if button == "options":
            return [(910, 645, 979, 707)]
        elif button == "download":
            return [(610, 690, 650, 726)]
        elif button == "subtitles":
            return [(153, 323), (345, 359)]
        else:
            return None

    def save_patches(self, patch: Image):
        patch.save(f"/tmp/patch_{self.patch_idx}.jpg")
        self.patch_idx = self.patch_idx + 1