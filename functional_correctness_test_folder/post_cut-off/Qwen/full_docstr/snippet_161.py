
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
        self.tools['add_tool'] = add_tool
        self.tools['PropertyList'] = PropertyList
        self.tools['Property'] = Property
        self.tools['PropertyType'] = PropertyType
