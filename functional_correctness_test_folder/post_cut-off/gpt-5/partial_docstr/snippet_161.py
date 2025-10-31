class BaziManager:

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self._tools = {}
        self.property_list = None

    def _safe_add_property(self, plist, prop):
        for method in ("add_property", "add", "append"):
            if hasattr(plist, method):
                try:
                    getattr(plist, method)(prop)
                    return True
                except Exception:
                    continue
        return False

    def _build_properties(self, PropertyList, Property, PropertyType):
        try:
            plist = None
            # Try common ctor patterns
            ctor_attempts = [
                lambda: PropertyList("八字命理工具"),
                lambda: PropertyList(title="八字命理工具"),
                lambda: PropertyList("八字命理工具", description="Bazi tools"),
                lambda: PropertyList(),
            ]
            for attempt in ctor_attempts:
                try:
                    plist = attempt()
                    break
                except Exception:
                    continue
            if plist is None:
                return None

            # Count property
            count_prop = None
            try:
                count_prop = Property(
                    "count",
                    getattr(PropertyType, "Integer", getattr(
                        PropertyType, "Int", None)),
                    name="工具数量",
                    readonly=True,
                    default=0,
                )
            except Exception:
                try:
                    count_prop = Property("count", name="工具数量")
                except Exception:
                    count_prop = None
            if count_prop is not None:
                self._safe_add_property(plist, count_prop)

            # List property
            list_prop = None
            try:
                list_prop = Property(
                    "tools",
                    getattr(PropertyType, "List", None),
                    name="工具列表",
                    readonly=True,
                    default=[],
                )
            except Exception:
                try:
                    list_prop = Property("tools", name="工具列表")
                except Exception:
                    list_prop = None
            if list_prop is not None:
                self._safe_add_property(plist, list_prop)

            return plist
        except Exception:
            return None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        # 构建属性列表（若外部类型不匹配则安全失败）
        self.property_list = self._build_properties(
            PropertyList, Property, PropertyType)

        # 注册管理器自身为一个工具入口
        try:
            add_tool("bazi.manager", self)
        except Exception:
            pass

    # 工具管理接口
    def register_tool(self, name, tool):
        if not isinstance(name, str) or not name:
            raise ValueError("工具名无效")
        self._tools[name] = tool

    def get_tool(self, name, default=None):
        return self._tools.get(name, default)

    def list_tools(self):
        return list(self._tools.keys())

    def __len__(self):
        return len(self._tools)
