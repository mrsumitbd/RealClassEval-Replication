
class BaziManager:

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = []

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        for prop in PropertyList:
            tool = add_tool(Property(prop, PropertyType))
            self.tools.append(tool)
