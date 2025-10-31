
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
        self.add_tool = add_tool
        self.PropertyList = PropertyList
        self.Property = Property
        self.PropertyType = PropertyType

        # 注册八字命理工具
        self.register_tools()

    def register_tools(self):
        '''
        注册八字命理工具。
        '''
        # 示例工具注册
        self.tools['天干'] = self.add_tool(
            name='天干',
            properties=self.PropertyList([
                self.Property('天干', self.PropertyType.STRING),
            ])
        )
        self.tools['地支'] = self.add_tool(
            name='地支',
            properties=self.PropertyList([
                self.Property('地支', self.PropertyType.STRING),
            ])
        )
        # 可以继续添加其他工具
