import urwid
from s_tui.sturwid.ui_elements import ViListBox

class HelpMenu:
    """HelpMenu is a widget containing instructions on usage of s-tui"""
    MAX_TITLE_LEN = 90

    def __init__(self, return_fn):
        self.return_fn = return_fn
        self.help_message = HELP_MESSAGE
        self.time_out_ctrl = urwid.Text(self.help_message)
        cancel_button = urwid.Button('Exit', on_press=self.on_cancel)
        cancel_button._label.align = 'center'
        if_buttons = urwid.Columns([cancel_button])
        title = urwid.Text(('bold text', '  Help Menu  \n'), 'center')
        self.titles = [title, self.time_out_ctrl, if_buttons]
        self.main_window = urwid.LineBox(ViListBox(self.titles))

    def get_size(self):
        """returns size of HelpMenu"""
        return (MESSAGE_LEN + 3, self.MAX_TITLE_LEN)

    def on_cancel(self, w):
        """Returns to original widget"""
        self.return_fn()