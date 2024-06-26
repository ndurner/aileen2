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
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', self.config_data['server'].get('aws_access_key_id'))
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', self.config_data['server'].get('aws_secret_access_key'))
        self.host = self.config_data['server']['host']
        self.port = self.config_data['server']['port']
        self.lm = self.config_data['implementations']['agent_lm']
        self.vlm = self.config_data['implementations']['vlm']
        self.ocr = self.config_data['implementations']['ocr']
        self.user_profiles = self.config_data["users"]

        # Load email configurations
        self.email_sender_name = self.config_data['email'].get('sender_name')
        self.email_sender_email = self.config_data['email'].get('sender_email')
    
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

    def get_email_config(self):
        return {
            "sender_name": self.email_sender_name,
            "sender_email": self.email_sender_email
        }