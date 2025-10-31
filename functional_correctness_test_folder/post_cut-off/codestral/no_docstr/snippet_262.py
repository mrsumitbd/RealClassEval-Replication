
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        print(f"SUCCESS: {message}")

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        print(f"WARNING: {message}")

    def error(self, message: str = 'An error occurred.'):
        print(f"ERROR: {message}")

    def skull(self, message: str = '💀'):
        print(f"SKULL: {message}")
