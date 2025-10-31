
class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        from bazi_tools import BaziTool1, BaziTool2, BaziTool3

        self.tools['tool1'] = BaziTool1()
        self.tools['tool2'] = BaziTool2()
        self.tools['tool3'] = BaziTool3()

        for tool_name, tool in self.tools.items():
            add_tool(tool_name, tool, PropertyList, Property, PropertyType)
