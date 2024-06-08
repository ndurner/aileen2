class LM:
    """Language model implementation"""

    def start_agent(self, user_task: str, screenshot_desc: str) -> str:
        """
        Kick-off agentic session by posing the user_task to the LM and
        offering tools.
        Returns the next function call for further processing, e.g. 'get_bundestag_transcript(...)'
        """
        pass

    def get_bundestag_transcript(self, url: str) -> str:
        """
        Corresponds to Agent task 'get_bundestag_transcript'.
        Returns the next function call for further processing, e.g. 'find_options_button(...)'
        """
        pass