
class BaziManager:

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        # 示例工具注册
        self.tools['天干'] = add_tool('天干', PropertyList, Property, PropertyType)
        self.tools['地支'] = add_tool('地支', PropertyList, Property, PropertyType)
        self.tools['五行'] = add_tool('五行', PropertyList, Property, PropertyType)
        self.tools['十神'] = add_tool('十神', PropertyList, Property, PropertyType)
        self.tools['纳音'] = add_tool('纳音', PropertyList, Property, PropertyType)
        self.tools['八字'] = add_tool('八字', PropertyList, Property, PropertyType)
