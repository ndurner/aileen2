from singleton_decorator import singleton
from lm import LM

class LM_Mock(LM):
    """
    Language model mock implementation.
    Canned responses from granite-8b-code-instruct
    """

    def start_agent(self, user_task: str, screenshot_desc: str) -> str:
        """
        Kick-off agentic session by posing the user_task to the LM and
        offering tools.
        Returns the next function call for further processing, e.g. 'get_bundestag_transcript(...)'
        """
        
        return 'get_bundestag_transcript("http://bundestag.de/video/123")'

    def get_bundestag_transcript(self, url: str) -> str:
        """
        Corresponds to Agent task 'get_bundestag_transcript'.
        Returns the next function call for further processing, e.g. 'find_options_button()'
        """

        return 'find_options_button()'