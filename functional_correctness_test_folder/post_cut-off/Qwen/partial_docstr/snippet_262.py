
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        print(f"Success: {message}")

    def warning(self, message: str = 'Holy! the dev forgot to write this warning message lol 💀.'):
        print(f"Warning: {message}")

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        print(f"Error: {message}")

    def skull(self, message: str = '💀'):
        print(f"Skull: {message}")
