class STMessages:
    '''A class to handle Streamlit messages.'''

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        try:
            import streamlit as st
            return st.success(message)
        except Exception:
            return None

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        '''Display a warning message.'''
        try:
            import streamlit as st
            return st.warning(message)
        except Exception:
            return None

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        try:
            import streamlit as st
            return st.error(message)
        except Exception:
            return None

    def skull(self, message: str = '💀'):
        '''Display a skull message.'''
        try:
            import streamlit as st
            return st.markdown(str(message))
        except Exception:
            return None
