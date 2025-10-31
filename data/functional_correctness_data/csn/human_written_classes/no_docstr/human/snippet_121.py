class switch_window:

    def __init__(self, browser, window_handle):
        self.browser = browser
        self.window_handle = window_handle

    def __enter__(self):
        self.current_window_handle = self.browser.driver.current_window_handle
        self.browser.driver.switch_to.window(self.window_handle)

    def __exit__(self, type, value, traceback):
        if self.current_window_handle in self.browser.driver.window_handles:
            self.browser.driver.switch_to.window(self.current_window_handle)