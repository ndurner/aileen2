from singleton_decorator import singleton
from lm_mock import LM_Mock
from vlm_mock import VLM_Mock
import ast
from typing import Any, Tuple
from PIL import Image

class WebAgent:
    """AI Agent driving tasks"""

    # FIXME: use real models
    lm = LM_Mock()
    vlm = VLM_Mock()
    cur_screenshot = Image.new("RGB", (200, 200))

    def start(self, task_prompt: str):
        next_step = self.lm.start_agent(task_prompt)
        tool_name, tool_args = self._parse_tool_call(next_step)

        if tool_name == "get_bundestag_transcript" and tool_args:
            self.get_bundestag_transcript(tool_args[0])

    def get_bundestag_transcript(self, url: str):
        next_step = self.lm.get_bundestag_transcript(url)
        tool_name, tool_args = self._parse_tool_call(next_step)

        if tool_name == "find_options_button":
            vlm_coords = self.vlm.scan_for_button(self.cur_screenshot, "options")
            if vlm_coords:
                logging.info(f"Found options button! {vlm_coords}")

    def _parse_tool_call(self, call_str: str) -> Tuple[Any, Any]:
        stree = ast.parse(call_str)
        for node in ast.walk(stree):
            if isinstance(node, ast.Call):
                tool_name = node.func.id
                tool_args = [ast.literal_eval(arg) for arg in node.args]

                return (tool_name, tool_args)
        
        return (None, None)