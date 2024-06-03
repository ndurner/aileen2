import json
import os
from dotenv import load_dotenv
from singleton_decorator import singleton

@singleton
class Config:
    """
    Configuration settings access
    """

    def __init__(self):
        load_dotenv()  # Load environment variables from .env
        self._load_configurations()

    def _load_configurations(self):
        # Load configurations from config.json
        with open('config.json') as config_file:
            self.config_data = json.load(config_file)

        # Environment variables override
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN', self.config_data['server'].get('twilio_auth_token'))
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY', self.config_data['ai'].get('nvidia_api_key'))
        self.openai_api_key = os.getenv('OPENAI_API_KEY', self.config_data['ai'].get('openai_api_key'))
        self.host = self.config_data['server']['host']
        self.port = self.config_data['server']['port']

    def get_twilio_auth_token(self):
        return self.twilio_auth_token

    def get_nvidia_api_key(self):
        return self.nvidia_api_key

    def get_openai_api_key(self):
        return self.openai_api_key

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port