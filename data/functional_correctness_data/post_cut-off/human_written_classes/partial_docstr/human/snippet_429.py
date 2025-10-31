from PySide6.QtCore import QTimer
from qtpy.QtGui import QIcon
import qtawesome as qta

class UIStateManager:
    """Manages UI state and control enable/disable logic."""

    def __init__(self, chat_window):
        from AgentCrew.modules.gui import ChatWindow
        if isinstance(chat_window, ChatWindow):
            self.chat_window = chat_window
        self.spinner_chars = ['⠉⠉', '⠈⠙', '⠀⠹', '⠀⢸', '⠀⣰', '⢀⣠', '⣀⣀', '⣄⡀', '⣆⠀', '⡇⠀', '⠏⠀', '⠋⠁']
        self.spinner_index = 0
        self._setup_animation_timer()

    def _setup_animation_timer(self):
        """Set up the animation timer for the stop button."""
        self.animation_timer = QTimer(self.chat_window)
        self.animation_timer.timeout.connect(self.update_send_button_text)

    def set_input_controls_enabled(self, enabled: bool):
        """Enable or disable input controls."""
        actual_enabled = enabled and (not self.chat_window.loading_conversation)
        self.chat_window.message_input.setEnabled(actual_enabled)
        self.chat_window.send_button.setEnabled(actual_enabled)
        self.chat_window.file_button.setEnabled(actual_enabled)
        self.chat_window.sidebar.setEnabled(actual_enabled)
        if actual_enabled:
            self._set_send_button_state()
            self.chat_window.message_input.setFocus()
            self.chat_window.file_button.setStyleSheet(self.chat_window.style_provider.get_button_style('secondary'))
        else:
            disabled_style = self.chat_window.style_provider.get_button_style('disabled')
            self.chat_window.send_button.setStyleSheet(disabled_style)
            self.chat_window.file_button.setStyleSheet(disabled_style)
        if not self.chat_window.loading_conversation:
            self.chat_window.waiting_for_response = not enabled

    def _set_send_button_state(self, is_stop_stated: bool=False):
        """Set the send button state (normal or stop mode)."""
        if not is_stop_stated:
            self.animation_timer.stop()
            send_icon = qta.icon('fa6s.paper-plane', color='white')
            self.chat_window.send_button.setIcon(send_icon)
            self.chat_window.send_button.setText('')
            self.chat_window.send_button.setStyleSheet(self.chat_window.style_provider.get_button_style('primary'))
            try:
                self.chat_window.send_button.clicked.disconnect()
            except Exception:
                pass
            self.chat_window.send_button.clicked.connect(self.chat_window.send_message)
        else:
            self.chat_window.send_button.setIcon(QIcon())
            self.chat_window.send_button.setText(f'{self.spinner_chars[-1]}')
            self.chat_window.send_button.setStyleSheet(self.chat_window.style_provider.get_button_style('stop'))
            self.animation_timer.setInterval(80)
            self.animation_timer.start()
            self.chat_window.send_button.clicked.disconnect()
            self.chat_window.send_button.clicked.connect(self.chat_window.stop_message_stream)
            self.chat_window.send_button.setEnabled(True)

    def update_send_button_text(self):
        """Cycle through spinner characters for stop button animation."""
        spinner_char = self.spinner_chars[self.spinner_index]
        self.chat_window.send_button.setText(f'{spinner_char}')
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)

    def stop_button_stopping_state(self):
        """Set button to stopping state."""
        if self.chat_window.waiting_for_response:
            self.chat_window.send_button.setDisabled(True)
            self.chat_window.send_button.setStyleSheet(self.chat_window.style_provider.get_button_style('stop_stopping'))