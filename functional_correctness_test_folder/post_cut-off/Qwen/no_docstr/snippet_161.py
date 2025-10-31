
class BaziManager:

    def __init__(self):
        self.tools = {}
        self.properties = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        if add_tool:
            self.tools[PropertyType] = PropertyList
        self.properties[PropertyType] = Property
