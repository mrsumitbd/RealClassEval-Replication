
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        print(f"✅ {message}")

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        print(f"⚠️ {message}")

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        print(f"❌ {message}")

    def skull(self, message: str = '💀'):
        print(f"💀 {message}")
