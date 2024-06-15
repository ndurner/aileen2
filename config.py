import json
import os
from dotenv import load_dotenv
from singleton_decorator import singleton

@singleton
class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env
        self._load_configurations()

    def _load_configurations(self):
        # Load configurations from config.json
        with open('config.json') as config_file:
            self.config_data = json.load(config_file)

        # Load other configurations
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN', self.config_data['server'].get('twilio_auth_token'))
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY', self.config_data['ai'].get('nvidia_api_key'))
        self.host = self.config_data['server']['host']
        self.port = self.config_data['server']['port']
        self.lm = self.config_data['implementations']['agent_lm']
        self.vlm = self.config_data['implementations']['vlm']
        self.ocr = self.config_data['implementations']['ocr']
        self.user_profiles = self.config_data["users"]

        # Load logging configurations
        self.log_level = self.config_data['logging']['level']
        self.log_format = self.config_data['logging']['format']
        self.log_datefmt = self.config_data['logging']['datefmt']
        self.log_filename = self.config_data['logging']['filename']
        self.log_filemode = self.config_data['logging']['filemode']

    def get_logging_config(self):
        return {
            "level": self.log_level,
            "format": self.log_format,
            "datefmt": self.log_datefmt,
            "filename": self.log_filename,
            "filemode": self.log_filemode
        }
    
    def get_ngc_config(self):
        ngc = self.config_data['implementations']['lm_ngc']
        return {
            "model": ngc['model'],
            "base_url": ngc['base_url'],
            "summarizer": {
                "model": ngc['summarizer']['model'],
                "base_url": ngc['summarizer']['base_url'],
            }
        }
    
    def get_vlm_config(self):
        ngc = self.config_data['implementations']['vlm_local']
        return {
            "model": ngc['model'],
        }
