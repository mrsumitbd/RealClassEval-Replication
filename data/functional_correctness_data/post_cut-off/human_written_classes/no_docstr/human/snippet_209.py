from gi.repository import Gtk, Adw, GtkSource, GLib, Gdk, GObject
from gradia.backend.settings import Settings

class FakeWindowManager:

    def __init__(self, source_view):
        self.source_view = source_view
        self.fake_window_container = None
        self.header_bar = None
        self.title_entry = None
        self.current_style_provider = None
        self.settings = Settings()

    def create_fake_window(self):
        if self.fake_window_container:
            return self.fake_window_container
        frame = Gtk.Frame(valign=Gtk.Align.START, margin_top=12)
        frame.add_css_class('window-border')
        frame.add_css_class('card')
        self.fake_window_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.fake_window_container.get_style_context().add_class('adw-window')
        self.header_bar = Adw.HeaderBar.new()
        self.header_bar.get_style_context().add_class('flat')
        self.title_entry = Gtk.Entry(xalign=0.5, focus_on_click=False)
        self.title_entry.set_text(self.settings.source_snippet_title)
        self.title_entry.set_halign(Gtk.Align.CENTER)
        self.title_entry.set_valign(Gtk.Align.CENTER)
        self.title_entry.set_width_chars(45)
        self.title_entry.set_max_length(100)
        self.title_entry.set_has_frame(False)
        self.title_entry.get_style_context().add_class('title')
        self.title_entry.get_style_context().add_class('title-entry')

        def on_title_entry_changed(entry):
            new_title = entry.get_text()
            self.settings.source_snippet_title = new_title
        self.title_entry.connect('changed', on_title_entry_changed)
        self.header_bar.set_title_widget(self.title_entry)
        source_view_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        source_view_container.append(self.source_view)
        self.fake_window_container.append(self.header_bar)
        self.fake_window_container.append(source_view_container)
        frame.set_child(self.fake_window_container)
        return frame

    def update_header_colors(self, style_scheme):
        if not self.header_bar or not self.title_entry:
            return
        if self.current_style_provider:
            self.header_bar.get_style_context().remove_provider(self.current_style_provider)
            self.title_entry.get_style_context().remove_provider(self.current_style_provider)
        bg_color, fg_color = self._extract_header_colors(style_scheme)
        if bg_color and fg_color:
            css_data = f'\n            headerbar {{\n                background: {bg_color};\n                color: {fg_color};\n                border-bottom: 1px solid alpha({fg_color}, 0.1);\n            }}\n\n            '
            self.current_style_provider = Gtk.CssProvider()
            self.current_style_provider.load_from_data(css_data.encode())
            self.header_bar.get_style_context().add_provider(self.current_style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.title_entry.get_style_context().add_provider(self.current_style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _extract_header_colors(self, style_scheme):
        scheme_id = style_scheme.get_id()
        text_style = style_scheme.get_style('text')
        bg_color = text_style.get_property('background')
        fg_color = text_style.get_property('foreground')
        return (bg_color, fg_color)

    def destroy_fake_window(self):
        if self.current_style_provider and self.header_bar:
            self.header_bar.get_style_context().remove_provider(self.current_style_provider)
            if self.title_entry:
                self.title_entry.get_style_context().remove_provider(self.current_style_provider)
        self.fake_window_container = None
        self.header_bar = None
        self.title_entry = None
        self.current_style_provider = None

    def get_container(self):
        return self.fake_window_container