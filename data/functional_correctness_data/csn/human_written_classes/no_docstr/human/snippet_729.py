import os
from getgauge import logger

class ScreenshotsStore:
    __screenshots = []

    @staticmethod
    def pending_screenshots():
        screenshots = ScreenshotsStore.__screenshots
        ScreenshotsStore.__screenshots = []
        return screenshots

    @staticmethod
    def capture():
        screenshot = ScreenshotsStore.capture_to_file()
        ScreenshotsStore.__screenshots.append(screenshot)

    @staticmethod
    def capture_to_file():
        if not registry.is_screenshot_writer:
            screenshot_file = _unique_screenshot_file()
            content = registry.screenshot_provider()()
            with open(screenshot_file, 'wb') as file:
                file.write(content)
            return os.path.basename(screenshot_file)
        screenshot_file = registry.screenshot_provider()()
        if not os.path.isabs(screenshot_file):
            screenshot_file = os.path.join(_screenshots_dir(), screenshot_file)
        if not os.path.exists(screenshot_file):
            logger.warning('Screenshot file {0} does not exists.'.format(screenshot_file))
        return os.path.basename(screenshot_file)

    @staticmethod
    def clear():
        ScreenshotsStore.__screenshots = []