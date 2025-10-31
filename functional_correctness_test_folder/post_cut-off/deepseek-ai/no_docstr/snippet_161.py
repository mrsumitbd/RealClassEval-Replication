
class BaziManager:

    def __init__(self):
        self.tools = []

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        tool = {
            'add_tool': add_tool,
            'PropertyList': PropertyList,
            'Property': Property,
            'PropertyType': PropertyType
        }
        self.tools.append(tool)
