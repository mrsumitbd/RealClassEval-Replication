from gi.repository import Gtk, Adw, GtkSource, GLib, Gdk, GObject

class StyleManager:

    def __init__(self):
        self.style_manager = GtkSource.StyleSchemeManager.get_default()
        self.style_manager.append_search_path('resource:///be/alexandervanhee/gradia/source-styles')
        self.settings = Gtk.Settings.get_default()
        self.theme_changed_callbacks = []
        self.style_schemes = ['Adwaita', 'classic', 'cobalt-light', 'kate', 'solarized-light', 'tango', 'Adwaita-dark', 'classic-dark', 'cobalt', 'kate-dark', 'oblivion', 'solarized-dark', 'clone-of-ubuntu', 'builder-dark', 'vscode-dark']
        self.use_generic_styles = True

    def get_all_schemes(self):
        return self.style_schemes