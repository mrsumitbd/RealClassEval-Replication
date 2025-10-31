class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        # 用于存储已注册的工具
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        # PropertyList 预期为可迭代的属性名列表
        # PropertyType 预期为属性名到类型的映射（可选）
        for prop_name in PropertyList:
            # 取得属性类型，若未指定则默认使用 str
            prop_type = PropertyType.get(prop_name, str) if isinstance(
                PropertyType, dict) else str
            # 创建 Property 实例
            prop = Property(name=prop_name, type=prop_type)
            # 简单的工具类，包含该属性
            tool_cls = type(
                f'{prop_name}Tool',
                (object,),
                {'property': prop}
            )
            # 注册工具
            add_tool(prop_name, tool_cls)
            # 记录到内部字典
            self.tools[prop_name] = tool_cls
        # 返回已注册工具列表，方便后续使用
        return self.tools
