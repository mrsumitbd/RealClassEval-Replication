
class BaziManager:

    def __init__(self):
        self.tools = []
        self.PropertyList = None
        self.Property = None
        self.PropertyType = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        self.PropertyList = PropertyList
        self.Property = Property
        self.PropertyType = PropertyType
        self.tools.append(add_tool)
