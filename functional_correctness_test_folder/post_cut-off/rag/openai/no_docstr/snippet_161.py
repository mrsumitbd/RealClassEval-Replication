class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        # 用于存储已注册的工具
        self._tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。

        Parameters
        ----------
        add_tool : callable
            用于将工具添加到外部系统的回调函数，接受一个工具实例。
        PropertyList : iterable
            由 (属性名, 属性类型标识) 组成的可迭代对象。
        Property : type
            用于创建属性实例的类，构造函数接受 (name, type)。
        PropertyType : dict
            将属性类型标识映射到实际 Python 类型的字典。
        '''
        for name, type_key in PropertyList:
            # 解析属性类型，若未找到则默认使用 str
            prop_type = PropertyType.get(type_key, str)
            # 创建属性实例
            prop = Property(name, prop_type)
            # 存储到内部字典，键为属性名
            self._tools[name] = prop
            # 调用外部回调注册工具
            add_tool(prop)

    def get_tool(self, name):
        '''
        根据属性名获取已注册的工具实例。

        Parameters
        ----------
        name : str
            属性名。

        Returns
        -------
        Property or None
            对应的工具实例，若不存在则返回 None。
        '''
        return self._tools.get(name)

    def __repr__(self):
        return f'<BaziManager with {len(self._tools)} tools>'
