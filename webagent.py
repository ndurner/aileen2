from singleton_decorator import singleton
from lm_mock import LM_Mock
from vlm_mock import VLM_Mock
from factory import Factory
import ast
from typing import Any, Tuple
from PIL import Image
import mylog
import time
import srt2txt
from emailsender import EMailSender

log = mylog.getLogger(__name__)

class WebAgent:
    """AI Agent driving tasks"""

    factory = Factory()
    lm = factory.provide_lm()
    vlm = factory.provide_vlm()
    webpage = factory.provide_browser()
    debug = False
    ocr = factory.provide_ocr()
    email_sender = EMailSender()

    target_audience = ""

    def start(self, task_prompt: str, user_profile: dict):
        self.target_audience = user_profile.get("profile", "(unknown)")
        self.user_email = user_profile.get("email")

        # determine next step
        next_step = self.lm.start_agent(task_prompt)
        tool_name, tool_args = self._parse_tool_call(next_step)

        if tool_name == "get_bundestag_transcript" and tool_args:
            self.get_bundestag_transcript(tool_args[0])
        elif tool_name == "report_error_to_user":
            error_msg = "Unknown error" if not tool_args else tool_args[0]
            self.report_error(error_msg)

    def get_bundestag_transcript(self, url: str):
        # load web page
        log.debug(f"Opening website {url}")
        self.webpage.open(url)

        time.sleep(5) # FIXME

        cur_screenshot = self.webpage.screenshot()
        if self.debug:
            cur_screenshot.save("/tmp/screenshot.png")

        # get web browser screenshot description
        desc = self.vlm.desc_en(cur_screenshot)
        log.debug(f"Screenshot described as '{desc}', determining next step")

        next_step = self.lm.get_bundestag_transcript(url, desc)
        tool_name, tool_args = self._parse_tool_call(next_step)
        log.debug(f"Tool to use: '{tool_name}', args: {tool_args}")

        if tool_name == "find_options_button":
            vlm_coords = self.vlm.scan_for_button(cur_screenshot, "options")
            if vlm_coords:
                log.info(f"Found options button! {vlm_coords}")
                elem = vlm_coords[0]
                self._browser_click(elem)

                self.get_dl_btn()
            else:
                self.report_error("Options/share button not found")
                return
        elif tool_name == "report_error_to_user":
            error_msg = "Unknown error" if not tool_args else tool_args[0]
            self.report_error(error_msg)
        else:
            self.report_error(f"LM requested unknown tool {tool_name} at get_bundestag_transcript()")

    def get_dl_btn(self):
        cur_screenshot = self.webpage.screenshot()
        if self.debug:
            cur_screenshot.save("/tmp/after_click.png")

        desc = self.vlm.desc_en(cur_screenshot)
        log.debug(f"Screenshot described as '{desc}', determining next step")
        next_step = self.lm.get_dl_btn(desc)
        tool_name, tool_args = self._parse_tool_call(next_step)
        log.debug(f"Tool to use: '{tool_name}', args: {tool_args}")

        if tool_name == "find_download_button":
            vlm_coords = self.vlm.scan_for_button(cur_screenshot, "download")
            if vlm_coords:
                log.info(f"Found downloads button! {vlm_coords}")
                elem = vlm_coords[0]
                self._browser_click(elem)

                self.get_subtitles_btn()
        elif tool_name == "report_error_to_user":
            error_msg = "Unknown error" if not tool_args else tool_args[0]
            self.report_error(error_msg)
        else:
            self.report_error(f"LM requested unknown tool {tool_name} at get_dl_btn()")

    def get_subtitles_btn(self):
        cur_screenshot = self.webpage.screenshot()
        if self.debug:
            cur_screenshot.save("/tmp/after_click.png")

        desc = self.vlm.desc_en(cur_screenshot)
        log.debug(f"Screenshot described as '{desc}', determining next step")

        next_step = self.lm.get_subtitles_btn(desc)
        tool_name, tool_args = self._parse_tool_call(next_step)
        log.debug(f"Tool to use: '{tool_name}', args: {tool_args}")

        if tool_name == "find_subtitles_button":
            srt_coords = self.ocr.scan_for_text(cur_screenshot, "Untertitel")
            if srt_coords:
                log.info(f"Found downloads button! {srt_coords}")
                elem = srt_coords[0]
                self._browser_click(elem)

                self.get_confirm_btn()
        elif tool_name == "report_error_to_user":
            error_msg = "Unknown error" if not tool_args else tool_args[0]
            self.report_error(error_msg)
        else:
            self.report_error(f"LM requested unknown tool {tool_name} at get_subtitles_btn()")

    def get_confirm_btn(self):
        cur_screenshot = self.webpage.screenshot()
        if self.debug:
            cur_screenshot.save("/tmp/after_click.png")

        desc = self.vlm.desc_en(cur_screenshot)
        log.debug(f"Screenshot described as '{desc}', determining next step")

        next_step = self.lm.get_confirm_btn(desc)
        tool_name, tool_args = self._parse_tool_call(next_step)
        log.debug(f"Tool to use: '{tool_name}', args: {tool_args}")

        if tool_name == "find_confirm_button":
            confirm_coords = self.ocr.scan_for_text(cur_screenshot, "Ja und herunterladen")
            if confirm_coords:
                log.info(f"Found confirm button! {confirm_coords}")
                elem = confirm_coords[0]
                self._browser_click(elem)

                self.summarize()
        elif tool_name == "report_error_to_user":
            error_msg = "Unknown error" if not tool_args else tool_args[0]
            self.report_error(error_msg)
        else:
            self.report_error(f"LM requested unknown tool {tool_name} at get_confirm_btn()")

    def summarize(self):
        dl_fn, payload = self.webpage.get_latest_download()
        if dl_fn.endswith(".srt"):
            payload = srt2txt.process(payload)

        resp = self.lm.summarize_for_audience(payload, self.target_audience)
        print(f"summarization result: {resp}")

        if self.user_email:
            self.email_sender.send_email(self.user_email, "Meeting summary", resp)
        else:
            log.warning("not sending E-Mail because no address is configured")

    def report_error(self, error_msg: str):
        log.error(f"Cannot operate webpage: {error_msg}")

        if self.user_email:
            self.email_sender.send_email(self.user_email, "Error", "An error has occured. Please check the logs.")

    def _parse_tool_call(self, call_str: str) -> Tuple[Any, Any]:
        stree = ast.parse(call_str.strip())
        for node in ast.walk(stree):
            if isinstance(node, ast.Call):
                tool_name = node.func.id
                tool_args = [ast.literal_eval(arg) for arg in node.args]

                return (tool_name, tool_args)
        
        return (None, None)
    
    def _browser_click(self, elem: Tuple[int, int, int, int]):
        coords = (((elem[0] + ((elem[2] - elem[0]) / 2.0)) / 2.0),
                  ((elem[1] + ((elem[3] - elem[1]) / 2.0)) / 2.0))
        self.webpage.click(coords)