from langchain_core.messages import HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from lm import LM
import lm_ngc_prompts
from config import Config

class LM_NGC(LM):
    """Agent language model implementation"""

    def __init__(self):
        general_config = Config()
        api_key = general_config.nvidia_api_key

        lm_config = general_config.get_ngc_config()

        self.ngc_llm = ChatNVIDIA(api_key = api_key, model = lm_config['model'], temperature = 0, stop = ["Question"])

    def start_agent(self, user_task: str) -> str:
        """
        Kick-off agentic session by posing the user_task to the LM and
        offering tools.
        Returns the next function call for further processing, e.g. 'get_bundestag_transcript(...)'
        """

        self.messages = [
            HumanMessage(content = lm_ngc_prompts.agent.format(user_task = user_task)),
        ]

        response = self.ngc_llm.invoke(self.messages)
        self.messages.extend([response])

        return response.content

    def get_bundestag_transcript(self, url: str, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_bundestag_transcript'.
        Returns the next function call for further processing, e.g. 'find_options_button(...)'
        """

        self.messages.extend([HumanMessage(
            content = lm_ngc_prompts.dl_btag.format(screenshot_description = screenshot_desc))])

        response = self.ngc_llm.invoke(self.messages)
        self.messages.extend([response])

    
    def get_dl_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_dl_btn'.
        Returns the next function call for further processing, e.g. 'find_download_button(...)'
        """

        self.messages.extend([HumanMessage(
            content = lm_ngc_prompts.dl_btn.format(screenshot_description = screenshot_desc))])

        response = self.ngc_llm.invoke(self.messages)
        self.messages.extend([response])

        return response.content
    
    def get_subtitles_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_dl_btn'.
        Returns the next function call for further processing, e.g. 'find_download_button(...)'
        """

        self.messages.extend([HumanMessage(
            content = lm_ngc_prompts.subtitles_btn.format(screenshot_description = screenshot_desc))])

        response = self.ngc_llm.invoke(self.messages)
        self.messages.extend([response])

        return response.content

    def get_confirm_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_dl_btn'.
        Returns the next function call for further processing, e.g. 'find_download_button(...)'
        """

        self.messages.extend([HumanMessage(
            content = lm_ngc_prompts.confirm_btn.format(screenshot_description = screenshot_desc))])

        response = self.ngc_llm.invoke(self.messages)
        self.messages.extend([response])

        return response.content

