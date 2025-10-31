class MultiSetWrapper:

    def __init__(self, main):
        """
        Args:
            main (NikkeConfig):
        """
        self.main = main
        self.in_wrapper = False

    def __enter__(self):
        if self.main.auto_update:
            self.main.auto_update = False
        else:
            self.in_wrapper = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.in_wrapper:
            self.main.update()
            self.main.auto_update = True