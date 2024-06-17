import os
import requests
import argparse
import tarfile
from tqdm import tqdm
import platform
from config import Config

general_config = Config()
vlm_config = general_config.get_vlm_config()

def download_vlm_from_url(url, save_path):
    print("Downloading VLM...")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check for request errors
        total_size_in_bytes = int(response.headers.get('content-length', 0))  # Get the total size of the file
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                progress_bar.update(len(chunk))  # Update the progress bar
                file.write(chunk)
        progress_bar.close()

        if progress_bar.n != total_size_in_bytes:
            print(f"ERROR: something went wrong during the download (incomplete?)")  # Check if the download was completed fully

    print(f"Downloaded from {url} to {save_path}")
    
    # Check if the downloaded file is a tar file and extract it
    if tarfile.is_tarfile(save_path):
        extract_vlm_dl(save_path)

def extract_vlm_dl(tar_path):
    # Define the target directory for extraction
    target_dir = os.path.expanduser("~/.cache/huggingface/hub/")
    os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists
    
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=target_dir)
    print(f"Extracted {tar_path} to {target_dir}")

def download_vlm_model(kaggle_username, kaggle_key, model_url=None):
    from transformers import PaliGemmaForConditionalGeneration, PaliGemmaProcessor
    PaliGemmaForConditionalGeneration.from_pretrained(vlm_config["model"])
    PaliGemmaProcessor.from_pretrained(vlm_config["model"])

def setup_ocr():
    import easyocr
    easyocr.Reader(['de'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download model and tokenizer")
    parser.add_argument("--vlm-model-url", required=False, help="Direct URL to download the model")
    args = parser.parse_args()

    if args.vlm_model_url:
        if args.vlm_model_url.startswith("http"):
            download_vlm_from_url(args.vlm_model_url, "/tmp/paligemma.tar")
        else:
            extract_vlm_dl(args.vlm_model_url)
    else:
        download_vlm_model()
