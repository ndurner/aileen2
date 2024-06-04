from singleton_decorator import singleton
import os

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "vlm.npz")

TOKENIZER_DIR = "tokenizer"
TOKENIZER_PATH = os.path.join(TOKENIZER_DIR, "vlm_tokenizer.model")

@singleton
class VLM:
    """Visual model implementation"""
