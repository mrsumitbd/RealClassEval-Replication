from etk.knowledge_graph.node import URI, Literal, LiteralType
from etk.knowledge_graph.subject import Subject

class DataValue:
    value = None
    full_value = None
    normalized_value = None
    type = None

    def _v_name(self):
        raise NotImplemented

    def _create_full_value(self):
        self.full_value = Subject(URI('wdv:' + self._v_name()))