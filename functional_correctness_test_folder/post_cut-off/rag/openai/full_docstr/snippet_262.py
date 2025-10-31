
import streamlit as st


class STMessages:
    """A class to handle Streamlit messages."""

    def success(self, message: str = "Operation completed successfully."):
        """Display a success message."""
        return st.success(message)

    def warning(self, message: str = "Holy! the dev forgot to write this warning messsage lol 💀."):
        """Display a warning message."""
        return st.warning(message)

    def error(self, message: str = "An error occurred."):
        """Display an error message."""
        return st.error(message)

    def skull(self, message: str = "💀"):
        """Display a skull message."""
        return st.write(message)
