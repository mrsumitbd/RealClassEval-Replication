
# st_messages.py

try:
    import streamlit as st
except Exception:  # pragma: no cover
    # Fallback stub that mimics the Streamlit API used here
    class _Stub:
        def success(self, msg):  # pragma: no cover
            print(f"[SUCCESS] {msg}")

        def warning(self, msg):  # pragma: no cover
            print(f"[WARNING] {msg}")

        def error(self, msg):  # pragma: no cover
            print(f"[ERROR] {msg}")

        def write(self, msg):  # pragma: no cover
            print(msg)

    st = _Stub()


class STMessages:
    """A class to handle Streamlit messages."""

    def success(self, message: str = "Operation completed successfully."):
        """Display a success message."""
        st.success(message)

    def warning(self, message: str = "Holy! the dev forgot to write this warning messsage lol 💀."):
        """Display a warning message."""
        st.warning(message)

    def error(self, message: str = "An error occurred."):
        """Display an error message."""
        st.error(message)

    def skull(self, message: str = "💀"):
        """Display a skull message."""
        st.write(message)
