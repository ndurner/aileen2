from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from browser import Browser
from typing import Tuple
from PIL import Image
import math
import io
import os

class Browser_Selenium(Browser):
    def __init__(self):
        from factory import Factory
        
        # Disable Selenium data collection
        os.environ["SE_AVOID_STATS"] = "true"

        opts = Options()
        opts.add_argument('--headless')  # Runs Chrome in headless mode.
        opts.add_argument('--no-sandbox')  # Bypass OS security model
        opts.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        opts.add_argument("--force-device-scale-factor=2")
        from webdriver_manager.chrome import ChromeDriverManager
        ChromeDriverManager().install()
        self.driver = webdriver.Chrome(options=opts)
        # size browser window approx. XGA resolution (1024x768), aligned to VLM
        self.driver.set_window_size(1024, 768)

    def open(self, url: str):
        """
        Open a web page
        """
        
        self.driver.get(url)

    def click(self, coords: Tuple[int, int]):
        """
        Perform click
        """
        
        action = ActionBuilder(self.driver)
        action.pointer_action.move_to_location(coords[0], coords[1])
        action.pointer_action.click()
        action.perform()

    def screenshot(self) -> Image:
        """
        Get screenshot
        """
        png = self.driver.get_screenshot_as_png()
        return Image.open(io.BytesIO(png))
