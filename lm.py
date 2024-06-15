class LM:
    """Language model implementation"""

    def start_agent(self, user_task: str) -> str:
        """
        Kick-off agentic session by posing the user_task to the LM and
        offering tools.
        Returns the next function call for further processing, e.g. 'get_bundestag_transcript(...)'
        """
        pass

    def get_bundestag_transcript(self, url: str, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_bundestag_transcript'.
        Returns the next function call for further processing, e.g. 'find_options_button(...)'
        """
        pass

    def get_subtitles_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_subtitles_btn'.
        Returns the next function call for further processing, e.g. 'find_subtitles_button(...)'
        """
        pass

    def get_confirm_btn(self, screenshot_desc: str) -> str:
        """
        Corresponds to Agent task 'get_confirmation_btn'.
        Returns the next function call for further processing, e.g. 'find_confirmation_button(...)'
        """
        pass
