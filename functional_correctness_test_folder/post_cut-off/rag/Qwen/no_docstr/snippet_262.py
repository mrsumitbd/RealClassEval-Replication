
import streamlit as st


class STMessages:
    '''A class to handle Streamlit messages.'''

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        st.success(message)

    def warning(self, message: str = 'Holy! the dev forgot to write this warning message lol 💀.'):
        '''Display a warning message.'''
        st.warning(message)

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        st.error(message)

    def skull(self, message: str = '💀'):
        '''Display a skull message.'''
        st.error(
            message)  # Streamlit does not have a specific skull icon method, so using error for demonstration
