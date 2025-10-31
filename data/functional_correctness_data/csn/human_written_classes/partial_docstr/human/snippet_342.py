class PyRadioThemeEditor:

    def __init__(self, *, theme_name, theme_path, editing, config, maxX, maxY):
        self.theme_name = theme_name
        self.theme_path = theme_path
        self.editing = editing
        self._cnf = config
        self.maxY = maxX
        self.maxY = maxY

    def keypress(self, char):
        """ PyRadioThemeEditor keypress """
        l_char = None