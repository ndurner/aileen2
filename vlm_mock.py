from singleton_decorator import singleton
from PIL import Image
import os
from vlm import VLM
from typing import Tuple

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "vlm.npz")

TOKENIZER_DIR = "tokenizer"
TOKENIZER_PATH = os.path.join(TOKENIZER_DIR, "vlm_tokenizer.model")

class VLM_Mock(VLM):
    """Visual model implementation"""

    def scan_for_button(self, image: Image, button: str) -> Tuple[int, int, int, int]:
        """
        Searches for a button that the model recognizes as 'button'.
        Returns button location
        """
        
        if button == "options":
            return (20, 20, 40, 40)
        else:
            return None
