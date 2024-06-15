from singleton_decorator import singleton
from lm import LM

class LM_Mock(LM):
    """
    Language model mock implementation.
    Canned responses from granite-8b-code-instruct
    """

    def start_agent(self, user_task: str) -> str:
        """
        Kick-off agentic session by posing the user_task to the LM and
        offering tools.
        Returns the next function call for further processing, e.g. 'get_bundestag_transcript(...)'
        """
        
        return 'get_bundestag_transcript("https://dbtg.tv/cvid/7611790")'

    def get_bundestag_transcript(self, url: str, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_bundestag_transcript'.
        Returns the next function call for further processing, e.g. 'find_options_button()'
        """

        return 'find_options_button()'
    
    def get_dl_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_dl_btn'.
        Returns the next function call for further processing, e.g. 'find_download_button(...)'
        """

        return 'find_download_button()'
    
    def get_subtitles_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_subtitles_btn'.
        Returns the next function call for further processing, e.g. 'find_subtitles_button(...)'
        """

        return 'find_subtitles_button()'

    def get_confirm_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_confirmation_btn'.
        Returns the next function call for further processing, e.g. 'find_confirm_button(...)'
        """

        return 'find_confirm_button()'

    def process_input_text(self, payload_input_text: str, task_description: str, target_audience: str) -> str:
        """
        Process, e.g. summarize, a long text for a specific audience
        """
        return "Mock LM text processing response"