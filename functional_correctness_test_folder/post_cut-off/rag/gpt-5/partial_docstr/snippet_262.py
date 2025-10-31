class STMessages:
    '''A class to handle Streamlit messages.'''

    def _emit(self, level: str, message: str):
        msg = str(message)
        try:
            import streamlit as st
        except Exception:
            st = None

        if st:
            if level == 'success':
                return st.success(msg)
            if level == 'warning':
                return st.warning(msg)
            if level == 'error':
                return st.error(msg)
            if level == 'skull':
                return st.write(msg)

        # Fallback to stdout if Streamlit is unavailable
        prefixes = {
            'success': 'SUCCESS',
            'warning': 'WARNING',
            'error': 'ERROR',
            'skull': ''
        }
        prefix = prefixes.get(level, '')
        print(f'{prefix + ": " if prefix else ""}{msg}')
        return None

    def success(self, message: str = 'Operation completed successfully.'):
        '''Display a success message.'''
        return self._emit('success', message)

    def warning(self, message: str = 'Holy! the dev forgot to write this warning messsage lol 💀.'):
        '''Display a warning message.'''
        return self._emit('warning', message)

    def error(self, message: str = 'An error occurred.'):
        '''Display an error message.'''
        return self._emit('error', message)

    def skull(self, message: str = '💀'):
        '''Display a skull message.'''
        return self._emit('skull', message)
