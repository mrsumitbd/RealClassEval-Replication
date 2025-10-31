from ofxstatement.ui import UI
from ofxstatement.parser import AbstractStatementParser
from collections.abc import MutableMapping

class Plugin:
    ui: UI

    def __init__(self, ui: UI, settings: MutableMapping) -> None:
        self.ui = ui
        self.settings = settings

    def get_parser(self, filename: str) -> AbstractStatementParser:
        raise NotImplementedError()