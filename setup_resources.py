import os
import requests
import argparse
import vlm
import requests
import platform
from webdriver_manager.chrome import ChromeDriverManager

def download_file_from_url(url, save_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check for request errors
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f"Downloaded from {url} to {save_path}")

def download_vlm_model(kaggle_username, kaggle_key, model_url=None):

    if not os.path.exists(vlm.MODEL_PATH):
        if not (args.kaggle_username or args.vlm_model_url):
            print("Warning: neither --kaggle-username/--kaggle-key nor --vlm-model-url given. Downloading VLM may fail.")

        if not os.path.exists(vlm.MODEL_DIR):
            os.makedirs(vlm.MODEL_DIR)
        
        if model_url:
            print(f"Downloading VLM checkpoint from {model_url}...")
            download_file_from_url(model_url, vlm.MODEL_PATH)
        else:
            print(f"Downloading VLM checkpoint from Kaggle...")
            if kaggle_username and kaggle_key:
                os.environ['KAGGLE_USERNAME'] = kaggle_username
                os.environ['KAGGLE_KEY'] = kaggle_key
            print("Downloading the checkpoint from Kaggle, this could take a few minutes....")
            if not os.path.exists(vlm.MODEL_DIR):
                os.makedirs(vlm.MODEL_DIR)

            import kagglehub
            MODEL_PATH = kagglehub.model_download('google/paligemma/jax/paligemma-3b-mix-448',
                                                  "./paligemma-3b-mix-448.bf16.npz")
            os.rename("./paligemma-3b-mix-448.bf16.npz", vlm.MODEL_PATH)

    # Download tokenizer
    if not os.path.exists(vlm.TOKENIZER_PATH):
        print("Downloading the model tokenizer...")
        if not os.path.exists(vlm.TOKENIZER_DIR):
            os.makedirs(vlm.TOKENIZER_DIR)
        os.system(f"gsutil cp gs://big_vision/paligemma_tokenizer.model {vlm.TOKENIZER_PATH}")
        print(f"Tokenizer path: {vlm.TOKENIZER_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download model and tokenizer")
    parser.add_argument("--kaggle-username", required=False, help="Kaggle username")
    parser.add_argument("--kaggle-key", required=False, help="Kaggle API key")
    parser.add_argument("--vlm-model-url", required=False, help="Direct URL to download the model")
    args = parser.parse_args()

    download_vlm_model(args.kaggle_username, args.kaggle_key, args.vlm_model_url)

    # attempt to install Chrome (which fails on macOS as of now)
    if platform.system() != 'Darwin':
        ChromeDriverManager().install()