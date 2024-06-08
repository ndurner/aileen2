from singleton_decorator import singleton
from lm import LM
from lm_mock import LM_Mock
from vlm import VLM
from vlm_mock import VLM_Mock
from config import Config


@singleton
class Factory:
    def __init__(self):
        self.conf = Config()

    def provide_lm(self) -> LM:
        lm = self.conf.lm
        if lm == "lm_mock":
            return LM_Mock()
        else:
            print(f"")
            return None
        
    def provide_vlm(self) -> VLM:
        vlm = self.conf.vlm
        if vlm == "vlm_mock":
            return VLM_Mock()
        else:
            return None
