class DisableLog:
    re_enable = False

    def __enter__(self):
        self.re_enable = _logger.is_on()
        off()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.re_enable:
            on()