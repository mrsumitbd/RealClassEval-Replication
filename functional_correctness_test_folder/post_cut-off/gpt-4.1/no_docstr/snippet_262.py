
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        return f"[SUCCESS] {message}"

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        return f"[WARNING] {message}"

    def error(self, message: str = 'An error occurred.'):
        return f"[ERROR] {message}"

    def skull(self, message: str = '💀'):
        return f"[SKULL] {message}"
