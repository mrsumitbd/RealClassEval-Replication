class STMessages:
    '''A class to handle Streamlit messages.'''

    def success(self, message: str = 'Operation completed successfully.') -> None:
        '''Display a success message.'''
        try:
            import streamlit as st
            st.success(message)
        except Exception:
            pass

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.') -> None:
        '''Display a warning message.'''
        try:
            import streamlit as st
            st.warning(message)
        except Exception:
            pass

    def error(self, message: str = 'An error occurred.') -> None:
        '''Display an error message.'''
        try:
            import streamlit as st
            st.error(message)
        except Exception:
            pass

    def skull(self, message: str = '💀') -> None:
        '''Display a skull message.'''
        try:
            import streamlit as st
            st.write(message)
        except Exception:
            pass
