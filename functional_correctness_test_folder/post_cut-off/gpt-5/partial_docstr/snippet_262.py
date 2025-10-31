class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        msg = f"✅ {str(message)}"
        print(msg)
        return msg

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        msg = f"⚠️ {str(message)}"
        print(msg)
        return msg

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        msg = f"❌ {str(message)}"
        print(msg)
        return msg

    def skull(self, message: str = '💀'):
        msg = f"💀 {str(message)}"
        print(msg)
        return msg
