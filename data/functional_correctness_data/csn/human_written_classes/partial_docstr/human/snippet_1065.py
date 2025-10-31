from xml.etree import ElementTree

class ToolBox:
    """
    Abstraction over a tool config file largely modelled after
    Galaxy's shed_tool_conf.xml. Hopefully over time this toolbox
    schema will be a direct superset of Galaxy's with extensions
    to support simple, non-toolshed based tool setups.
    """

    def __init__(self, path_string):
        self.tool_configs = []
        paths = [path.strip() for path in path_string.split(',')]
        for path in paths:
            toolbox_tree = ElementTree.parse(path)
            toolbox_root = toolbox_tree.getroot()
            tool_path = toolbox_root.get('tool_path')
            self.__load_tools_from_els(toolbox_root, tool_path)

    def __load_tools_from_els(self, toolbox_root, tool_path):
        els = toolbox_root.findall('tool')
        for el in els:
            try:
                if 'guid' in el.attrib:
                    tool_cls = ToolShedToolConfig
                else:
                    tool_cls = SimpleToolConfig
                tool = tool_cls(el, tool_path)
                self.tool_configs.append(tool)
            except Exception:
                log.exception('Failed to load tool.')

    def get_tool(self, id):
        tools = self.__find_tools_by_id(id)
        if not tools:
            raise KeyError("Failed to find tool with id '%s'" % id)
        if len(tools) > 1:
            log.warn("Found multiple tools with id '%s', returning first." % id)
        return tools[0]

    def __find_tools_by_id(self, id):
        return [tool for tool in self.tool_configs if tool.id == id]