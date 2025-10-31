
import streamlit as st


class STMessages:
    '''A class to handle Streamlit messages.'''

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        st.success(message)

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        '''Display a warning message.'''
        st.warning(message)

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        st.error(message)

    def skull(self, message: str = '💀'):
        '''Display a skull message.'''
        st.error(message)

# Example usage:


def main():
    st_messages = STMessages()
    st_messages.success('This is a success message.')
    st_messages.warning('This is a warning message.')
    st_messages.error('This is an error message.')
    st_messages.skull('This is a skull message.')


if __name__ == '__main__':
    main()
