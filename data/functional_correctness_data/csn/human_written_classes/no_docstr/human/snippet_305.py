class ThreadingManager:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def dict(self, *args, **kwargs):
        return dict(*args, **kwargs)