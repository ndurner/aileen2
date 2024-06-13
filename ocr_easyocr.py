from PIL import Image
from typing import List, Tuple
import easyocr
from ocr import OCR
import numpy as np

class OCR_EasyOCR(OCR):
    """Visual model implementation"""

    def scan_for_text(self, image: Image, search_text: str) -> List[Tuple[int, int, int, int]]:
        """
        Searches for the specified text {search_text} in the image.
        Returns a list of text locations (bounding boxes).
        """
        
        reader = easyocr.Reader(['de'])
        results = reader.readtext(np.array(image))

        found_texts = []

        for (bbox, detected_text, prob) in results:
            if prob >= 0.5:  # Confidence threshold
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))

                if detected_text.startswith(search_text):
                    found_texts.append((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
        
        return found_texts