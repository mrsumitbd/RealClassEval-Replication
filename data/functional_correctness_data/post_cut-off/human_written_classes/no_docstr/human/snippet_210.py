from gi.repository import Gtk, Adw, GtkSource, GLib, Gdk, GObject

class LanguageManager:

    def __init__(self):
        self.lang_manager = GtkSource.LanguageManager.get_default()
        self.languages = sorted(self.lang_manager.get_language_ids())

    def get_languages(self):
        return self.languages

    def get_language(self, lang_id):
        return self.lang_manager.get_language(lang_id)