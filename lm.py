class LM:
    """Language model implementation"""

    def get_ctx_len_for_model(self, model: str) -> int:
        return {
            "google/codegemma-1.1-7b": 4096,
            "google/codegemma-7b": 4096,
            "google/gemma-2b": 4096,            # API endpoint rejects > 4096
            "google/gemma-7b": 4096,            # API endpoint rejects > 4096
            "ibm/granite-34b-code-instruct": 6100, # roughly
            "ibm/granite-8b-code-instruct": 4096,
            "meta/codellama-70b": 4096, # CHECK
            "meta/llama2-70b": 4096, # CHECK
            "meta/llama3-70b-instruct": 8192,
            "meta/llama3-8b-instruct": 8192,
            "microsoft/phi-3-medium-4k-instruct": 4096,
            "microsoft/phi-3-mini-128k-instruct": 60000,
            "microsoft/phi-3-mini-4k-instruct": 2048,
            "microsoft/phi-3-small-128k-instruct": 16000,
            "microsoft/phi-3-small-8k-instruct": 8192,
            "mistralai/mistral-7b-instruct-v0.2": 16375,
            "mistralai/mistral-large": 16375, # TODO: roughly based on v2 tokenizer, which isn't on HF?
            "mistralai/mixtral-8x22b-instruct-v0.1": 21100, # roughly
            "mistralai/mixtral-8x22b-v0.1": 21100, # roughly
            "mistralai/mixtral-8x7b-instruct-v0.1": 16384,
        }.get(model)
    
    def get_tokenizer_for_model(self, model: str) -> str:
        return {
            "google/codegemma-1.1-7b": "philschmid/gemma-tokenizer-chatml",
            "google/codegemma-7b": "philschmid/gemma-tokenizer-chatml",
            "google/gemma-2b": "philschmid/gemma-tokenizer-chatml",
            "google/gemma-7b": "philschmid/gemma-tokenizer-chatml",
            "ibm/granite-8b-code-instruct": "ibm-granite/granite-8b-code-instruct",
            "ibm/granite-34b-code-instruct": "ibm-granite/granite-8b-code-instruct",
            "meta/llama3-70b-instruct": "philschmid/meta-llama-3-tokenizer",
            "meta/llama3-8b-instruct": "philschmid/meta-llama-3-tokenizer",
            "mistralai/mistral-7b-instruct-v0.2": "mistral-community/Mistral-7B-v0.2",
            "mistralai/mixtral-8x22b-instruct-v0.1": "Xenova/mistral-tokenizer-v3",
            "mistralai/mixtral-8x22b-v0.1": "Xenova/mistral-tokenizer-v3",
            "mistralai/mixtral-8x7b-instruct-v0.1": "TheBloke/Mixtral-8x7B-v0.1-GPTQ",
        }.get(model, model)

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

    def summarize_for_audience(self, payload_input_text: str, target_audience: str) -> str:
        """
        Summarize a long text for a specific audience
        """
        pass