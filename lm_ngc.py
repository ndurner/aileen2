from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from transformers import AutoTokenizer
from lm import LM
import lm_ngc_prompts
from config import Config

class LM_NGC(LM):
    """Agent language model implementation"""

    def __init__(self):
        general_config = Config()
        api_key = general_config.nvidia_api_key

        lm_config = general_config.get_ngc_config()
        lm_config_sum = lm_config['summarizer']
        self.max_out_tokens = 1000 # FIXME

        self.ngc_llm = ChatNVIDIA(api_key = api_key, model = lm_config['model'], temperature = 0.1)
        self.ngc_llm_sum = ChatNVIDIA(api_key = api_key, model = lm_config_sum['model'], temperature = 0.7, max_tokens = self.max_out_tokens)

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

        return response.content
    
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

    def summarize_for_audience(self, payload_input_text: str, target_audience: str) -> str:
        """
        Summarize a long text for a specific audience
        """
        
        prompt_template = PromptTemplate.from_template(lm_ngc_prompts.process_text_setup, partial_variables = {
            "user_profile": target_audience
        })
        refine_prompt_template = PromptTemplate.from_template(lm_ngc_prompts.process_text_refine, partial_variables = {
            "user_profile": target_audience
        })

        tok = AutoTokenizer.from_pretrained(self.get_tokenizer_for_model(self.ngc_llm_sum.model))
        tok_prompt = tok.encode(prompt_template.format(text = "", part_number="183"))
        tok_refine = tok.encode(refine_prompt_template.format(text = "", existing_part = "", part_number="183"))
        max_split_len = self.get_ctx_len_for_model(self.ngc_llm_sum.model) - max([len(tok_prompt), len(tok_refine)]) - self.max_out_tokens

        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(tok, chunk_size = max_split_len, chunk_overlap = 0)
        split_text = text_splitter.split_text(payload_input_text)

        template = prompt_template
        summary = str()
        for idx, split in enumerate(split_text):
            prompt = template.format_prompt(text = split, part_number = idx + 1)

            response = self.ngc_llm_sum.invoke(prompt)
            summary = response.content

            template = refine_prompt_template.partial(existing_part = summary)

        return summary
