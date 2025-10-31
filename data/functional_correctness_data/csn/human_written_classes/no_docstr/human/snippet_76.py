from gi.repository import Gdk

class NotebookScrollCallback:

    def __init__(self, notebook):
        self.notebook = notebook

    def on_scroll(self, widget, event):
        direction = event.get_scroll_direction().direction
        if direction is Gdk.ScrollDirection.DOWN or direction is Gdk.ScrollDirection.RIGHT:
            self.notebook.next_page()
        else:
            self.notebook.prev_page()
        return True