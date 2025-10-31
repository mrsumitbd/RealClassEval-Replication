
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        return f"✅ {message}"

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        return f"⚠️ {message}"

    def error(self, message: str = 'An error occurred.'):
        return f"❌ {message}"

    def skull(self, message: str = '💀'):
        return f"💀 {message}"
