
class BaziManager:

    def __init__(self):
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        self.PropertyList = PropertyList
        self.Property = Property
        self.PropertyType = PropertyType
        self.add_tool = add_tool
        self._initialize_tools()

    def _initialize_tools(self):
        for prop in self.PropertyList:
            tool = self.add_tool(prop, self.Property, self.PropertyType)
            self.tools[prop] = tool
