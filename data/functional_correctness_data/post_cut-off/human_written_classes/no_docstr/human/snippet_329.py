import numpy as np
import win32gui
import pyautogui
from desktopmagic.screengrab_win32 import getDisplayRects

class Screenshot:

    @staticmethod
    def is_application_fullscreen(window):
        screen_width, screen_height = pyautogui.size()
        return (window.width, window.height) == (screen_width, screen_height)

    @staticmethod
    def get_window_real_resolution(window):
        left, top, right, bottom = win32gui.GetClientRect(window._hWnd)
        return (right - left, bottom - top)

    @staticmethod
    def get_window_region(window):
        if Screenshot.is_application_fullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            real_width, real_height = Screenshot.get_window_real_resolution(window)
            other_border = (window.width - real_width) // 2
            up_border = window.height - real_height - other_border
            return (window.left + other_border, window.top + up_border, window.width - other_border - other_border, window.height - up_border - other_border)

    @staticmethod
    def get_window(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window
        return False

    @staticmethod
    def get_main_screen_location():
        rects = getDisplayRects()
        min_x = min([rect[0] for rect in rects])
        min_y = min([rect[1] for rect in rects])
        return (-min_x, -min_y)

    @staticmethod
    def take_screenshot(title, resolution, screens=False, crop=(0, 0, 1, 1)):
        window = Screenshot.get_window(title)
        if window:
            left, top, width, height = Screenshot.get_window_region(window)
            if screens:
                offset_x, offset_y = Screenshot.get_main_screen_location()
            else:
                offset_x, offset_y = (0, 0)
            screenshot = pyautogui.screenshot(region=(int(left + width * crop[0] + offset_x), int(top + height * crop[1] + offset_y), int(width * crop[2]), int(height * crop[3])), allScreens=screens)
            real_width, _ = Screenshot.get_window_real_resolution(window)
            if real_width > resolution[0]:
                screenshot_scale_factor = resolution[0] / real_width
                screenshot = screenshot.resize((int(resolution[0] * crop[2]), int(resolution[1] * crop[3])))
            else:
                screenshot_scale_factor = 1
            screenshot_pos = (int(left + width * crop[0]), int(top + height * crop[1]), int(width * crop[2] * screenshot_scale_factor), int(height * crop[3] * screenshot_scale_factor))
            return (np.array(screenshot), screenshot_pos, screenshot_scale_factor)
        return False