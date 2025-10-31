
class STMessages:

    def success(self, message: str = 'Operation completed successfully.'):
        print(f'\033[92mSUCCESS: {message}\033[0m')

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        print(f'\033[93mWARNING: {message}\033[0m')

    def error(self, message: str = 'An error occurred.'):
        print(f'\033[91mERROR: {message}\033[0m')

    def skull(self, message: str = '💀'):
        print(f'\033[91m{message}\033[0m')


# Example usage:
if __name__ == "__main__":
    st_messages = STMessages()
    st_messages.success()
    st_messages.warning()
    st_messages.error()
    st_messages.skull('Something went terribly wrong!')
