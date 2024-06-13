from PIL import Image
from typing import List, Tuple
from ocr import OCR

class OCR_Mock(OCR):
    """Visual model implementation"""

    def scan_for_text(self, image: Image, text: str) -> List[Tuple[int, int, int, int]]:
        """
        Searches for text {text}
        Returns text location
        """
        
        if text == "Untertitel":
            return [(426, 818, 730, 850)]
        elif text == "Ja und herunterladen":
            return [(154, 960, 384, 986)]
        else:
            return None
