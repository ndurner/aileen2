from PIL import Image
from typing import List, Tuple

class OCR:
    """Visual model implementation"""

    def scan_for_text(self, image: Image, text: str) -> List[Tuple[int, int, int, int]]:
        """
        Searches for text {text}
        Returns text location
        """
        pass