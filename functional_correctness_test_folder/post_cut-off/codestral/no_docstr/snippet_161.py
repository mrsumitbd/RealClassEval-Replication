
class BaziManager:

    def __init__(self):

        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):

        for tool_name, tool_properties in add_tool.items():
            self.tools[tool_name] = {}
            for prop_name, prop_value in tool_properties.items():
                if prop_name in PropertyList:
                    self.tools[tool_name][prop_name] = Property(
                        prop_value, PropertyType)
