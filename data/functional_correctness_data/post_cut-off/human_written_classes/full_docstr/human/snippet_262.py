import streamlit as st

class STMessages:
    """A class to handle Streamlit messages."""

    def success(self, message: str='Operation completed successfully.'):
        """Display a success message."""
        st.success(message, icon='✅')

    def warning(self, message: str='Holy! the dev forgot to write this warning messsage lol 💀.'):
        """Display a warning message."""
        st.warning(message, icon='⚠️')

    def error(self, message: str='An error occurred.'):
        """Display an error message."""
        st.error(message, icon='❌')

    def skull(self, message: str='💀'):
        """Display a skull message."""
        st.info(message, icon='💀')