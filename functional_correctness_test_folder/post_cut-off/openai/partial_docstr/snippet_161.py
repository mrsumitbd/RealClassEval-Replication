
class BaziManager:
    """
    八字管理器，用于初始化并注册所有八字命理工具。
    """

    def __init__(self):
        """
        初始化八字管理器。
        """
        # 用于存放已注册的工具
        self.tools = {}
        # 记录工具相关信息，供后续使用
        self.property_list = None
        self.property_class = None
        self.property_type = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册所有八字命理工具。

        Parameters
        ----------
        add_tool : Callable[[str, Any], None]
            用于将工具注册到管理器的回调函数，通常会把工具存入 `self.tools`。
        PropertyList : Iterable
            工具属性列表，支持两种形式：
            1. 迭代器中每个元素为 ``(name, type_key)`` 的元组或列表。
            2. 仅包含属性名的字符串列表，类型将从 `PropertyType` 中查找。
        Property : Callable
            工具类或工厂，用于创建工具实例。调用方式为 ``Property(name, type_obj)``。
        PropertyType : Mapping
            用于将类型键映射为实际类型对象的字典或映射。
        """
        # 保存工具相关信息
        self.property_list = PropertyList
        self.property_class = Property
        self.property_type = PropertyType

        for item in PropertyList:
            # 解析属性名与类型
            if isinstance(item, (list, tuple)) and len(item) == 2:
                prop_name, type_key = item
            else:
                prop_name = item
                type_key = None

            # 根据 type_key 获取实际类型对象
            if type_key is not None:
                type_obj = PropertyType.get(type_key, type_key)
            else:
                # 如果没有提供类型键，直接使用 PropertyType 作为类型
                type_obj = PropertyType

            # 创建工具实例
            prop_instance = Property(prop_name, type_obj)

            # 注册工具
            add_tool(prop_name, prop_instance)

            # 同时保存在本地字典中，方便后续访问
            self.tools[prop_name] = prop_instance
