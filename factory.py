from singleton_decorator import singleton
from lm import LM
from lm_mock import LM_Mock
from lm_ngc import LM_NGC
from vlm import VLM
from vlm_mock import VLM_Mock
from vlm_hf import VLM_HF
from ocr import OCR
from ocr_mock import OCR_Mock
from ocr_easyocr import OCR_EasyOCR
from browser import Browser
from browser_selenium import Browser_Selenium
from config import Config
import mylog

log = mylog.getLogger(__name__)

@singleton
class Factory:
    def __init__(self):
        self.conf = Config()

    def provide_lm(self) -> LM:
        lm = self.conf.lm
        if lm == "lm_mock":
            return LM_Mock()
        elif lm == "lm_ngc":
            return LM_NGC()
        else:
            log.error(f"LM '{lm}' not found")
            return None
        
    def provide_vlm(self) -> VLM:
        vlm = self.conf.vlm
        if vlm == "vlm_mock":
            return VLM_Mock()
        elif vlm == "vlm_hf":
            return VLM_HF()
        else:
            return None
        
    def provide_ocr(self) -> OCR:
        ocr = self.conf.ocr
        if ocr == "ocr_mock":
            return OCR_Mock()
        elif ocr == "ocr_easyocr":
            return OCR_EasyOCR()
        else:
            return None

    def provide_browser(self) -> Browser:
        return Browser_Selenium()