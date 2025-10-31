class _StorageAccountStats:

    def __init__(self):
        self.success_count = 0
        self.total_count = 0

    def log_result(self, success: bool):
        self.total_count += 1
        if success:
            self.success_count += 1

    def reset(self):
        self.success_count = 0
        self.total_count = 0