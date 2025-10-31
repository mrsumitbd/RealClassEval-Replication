from PyQt6.QtGui import QFont, QFontDatabase

class ReTextSettings:

    def __init__(self, settings, defaults):
        object.__setattr__(self, 'settings', settings)
        object.__setattr__(self, 'defaults', defaults)
        for option in defaults:
            default = defaults[option]
            if isinstance(default, list):
                object.__setattr__(self, option, readListFromSettings(option, settings=settings))
            else:
                object.__setattr__(self, option, readFromSettings(option, type(default), default=default, settings=settings))

    def __setattr__(self, option, value):
        if option not in self.defaults:
            raise AttributeError('Unknown attribute')
        default = self.defaults[option]
        if isinstance(default, list):
            object.__setattr__(self, option, value.copy())
            writeListToSettings(option, value, settings=self.settings)
        else:
            object.__setattr__(self, option, value)
            writeToSettings(option, value, default=default, settings=self.settings)

    def getPreviewFont(self):
        font = QFont()
        if self.font:
            font.fromString(self.font)
        return font

    def getEditorFont(self):
        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        if self.editorFont:
            font.fromString(self.editorFont)
        return font