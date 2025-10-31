class FakeVimMode:

    @staticmethod
    def init(window):
        window.setStatusBar(StatusBar())

    @staticmethod
    def exit(window):
        window.statusBar().deleteLater()