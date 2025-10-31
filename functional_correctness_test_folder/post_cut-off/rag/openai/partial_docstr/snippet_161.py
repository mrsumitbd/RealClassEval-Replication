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

        Parameters
        ----------
        add_tool : callable
            用于将工具添加到系统的回调函数，签名应为 ``add_tool(name, property_obj)``。
        PropertyList : Iterable
            包含工具属性定义的可迭代对象。每个元素可以是
            - 字典，键为 ``name`` 与 ``type``（可选，默认 ``'string'``）
            - 元组 ``(name, type)``
        Property : type
            用于创建属性实例的类，构造函数至少接受 ``name`` 与 ``type`` 两个参数。
        PropertyType : type
            用于包装属性类型的类，构造函数接受原始类型字符串。
        '''
        for prop_def in PropertyList:
            # 解析工具名称与类型
            if isinstance(prop_def, dict):
                name = prop_def.get('name')
                ptype = prop_def.get('type', 'string')
            else:
                # 预期为 (name, type) 形式
                name, ptype = prop_def

            # 创建 PropertyType 与 Property 实例
            prop_type_obj = PropertyType(ptype)
            prop_obj = Property(name=name, type=prop_type_obj)

            # 注册工具
            add_tool(name, prop_obj)

            # 记录到本地字典，方便后续查询
            self.tools[name] = prop_obj
        # 返回 None，保持与原始接口兼容
        return None
