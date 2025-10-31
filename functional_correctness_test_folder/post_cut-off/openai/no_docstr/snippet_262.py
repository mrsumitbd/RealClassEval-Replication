class STMessages:
    def success(self, message: str = 'Operation completed successfully.'):
        """Return a formatted success message."""
        return f"✅ {message}"

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        """Return a formatted warning message."""
        return f"⚠️ {message}"

    def error(self, message: str = 'An error occurred.'):
        """Return a formatted error message."""
        return f"❌ {message}"

    def skull(self, message: str = '💀'):
        """Return a formatted skull message."""
        return f"💀 {message}"
