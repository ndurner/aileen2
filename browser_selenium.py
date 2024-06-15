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
import tempfile
import shutil

class Browser_Selenium(Browser):
    download_dir = ""

    def __init__(self):
        from factory import Factory
        
        # Disable Selenium data collection
        os.environ["SE_AVOID_STATS"] = "true"

        self.download_dir = tempfile.mkdtemp()

        opts = Options()
        opts.add_argument('--headless')  # Runs Chrome in headless mode.
        opts.add_argument('--no-sandbox')  # Bypass OS security model
        opts.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        opts.add_argument("--force-device-scale-factor=2")

        opts.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(options=opts)
        # size browser window approx. XGA resolution (1024x768), aligned to VLM
        self.driver.set_window_size(1024, 768)

    def __del__(self):
        shutil.rmtree(self.download_dir, ignore_errors = True)

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
        ActionChains(self.driver).pause(0.5).perform()

    def screenshot(self) -> Image:
        """
        Get screenshot
        """
        png = self.driver.get_screenshot_as_png()
        return Image.open(io.BytesIO(png))

    def get_latest_download(self) -> Tuple[str, str]:
        """
        Retrieve the file name and content of the most recently downloaded file
        """
        # List all files sorted by modification time
        files = sorted(os.listdir(self.download_dir), key=lambda x: os.path.getmtime(os.path.join(self.download_dir, x)))

        # Get the latest file based on the last modification time
        latest_file_path = os.path.join(self.download_dir, files[-1]) if files else None

        if latest_file_path:
            with open(latest_file_path, 'rt') as file:
                content = file.read()
                return (latest_file_path, content)
        
        return (None, None)