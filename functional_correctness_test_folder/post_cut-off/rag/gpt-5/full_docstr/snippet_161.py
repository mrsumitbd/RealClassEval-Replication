class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = []
        self._initialized = False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        if self._initialized:
            return

        # 构建通用的出生信息属性列表
        birth_props = self._build_birth_properties(
            PropertyList, Property, PropertyType)

        # 工具定义
        tools = [
            {
                'id': 'bazi_chart',
                'name': '八字排盘',
                'description': '根据出生信息生成四柱八字与天干地支。',
                'props': birth_props,
                'meta': {'version': '1.0.0', 'category': '命盘'}
            },
            {
                'id': 'ten_gods',
                'name': '十神分析',
                'description': '基于命盘分析十神格局与用神。',
                'props': birth_props,
                'meta': {'version': '1.0.0', 'category': '分析'}
            },
            {
                'id': 'luck_pillars',
                'name': '大运流年',
                'description': '推算大运、流年、流月变化趋势。',
                'props': self._extend_with_years(birth_props, PropertyList, Property, PropertyType),
                'meta': {'version': '1.0.0', 'category': '流年'}
            },
        ]

        for t in tools:
            self._register_tool(
                add_tool, t['id'], t['name'], t['description'], t['props'], t['meta'])
            self.tools.append({
                'id': t['id'],
                'name': t['name'],
                'description': t['description']
            })

        self._initialized = True

    # ------------------------------
    # Helpers
    # ------------------------------

    def _build_birth_properties(self, PropertyList, Property, PropertyType):
        plist = self._safe_make_property_list(PropertyList)

        dt_type = self._get_property_type(
            PropertyType, ['DATETIME', 'DATE', 'STRING'])
        enum_type = self._get_property_type(
            PropertyType, ['ENUM', 'CHOICE', 'SELECT', 'STRING'])
        str_type = self._get_property_type(PropertyType, ['STRING'])
        tz_type = self._get_property_type(PropertyType, ['STRING'])
        cal_type = self._get_property_type(
            PropertyType, ['ENUM', 'CHOICE', 'SELECT', 'STRING'])

        props = [
            self._make_property(
                Property, PropertyType, 'birth_datetime', '出生日期时间', dt_type, required=True),
            self._make_property(Property, PropertyType, 'gender', '性别', enum_type, required=False,
                                options=[('male', '男'), ('female', '女'), ('unknown', '未知')]),
            self._make_property(Property, PropertyType, 'timezone',
                                '时区', tz_type, required=False, default='Asia/Shanghai'),
            self._make_property(Property, PropertyType, 'calendar', '历法', cal_type, required=False,
                                default='solar', options=[('solar', '公历'), ('lunar', '农历')]),
            self._make_property(Property, PropertyType,
                                'location', '出生地', str_type, required=False),
        ]

        for p in props:
            self._property_list_add(plist, p)

        return plist

    def _extend_with_years(self, base_plist, PropertyList, Property, PropertyType):
        # 复制一个列表/PropertyList，避免修改原有
        new_plist = self._clone_property_list(base_plist, PropertyList)

        int_type = self._get_property_type(
            PropertyType, ['INT', 'INTEGER', 'NUMBER', 'FLOAT', 'STRING'])
        years_prop = self._make_property(
            Property, PropertyType, 'years', '推算年数', int_type, required=False, default=10)
        self._property_list_add(new_plist, years_prop)
        return new_plist

    def _register_tool(self, add_tool, tool_id, name, description, prop_list, meta):
        # 优先尝试通过关键字参数注册
        kwargs = {
            'tool_id': tool_id,
            'name': name,
            'title': name,
            'label': name,
            'description': description,
            'properties': prop_list,
            'props': prop_list,
            'property_list': prop_list,
            'meta': meta,
            'manager': self,
        }

        # 尝试匹配 add_tool 的参数
        try:
            import inspect
            sig = inspect.signature(add_tool)
            accepted = set(sig.parameters.keys())
            filtered = {k: v for k, v in kwargs.items() if k in accepted}
            if filtered:
                add_tool(**filtered)
                return
        except Exception:
            pass

        # 依次尝试几种常见位置参数签名
        for args in (
            (tool_id, name, description, prop_list, meta),
            (tool_id, name, description, prop_list),
            (tool_id, name, prop_list),
            (tool_id, prop_list),
        ):
            try:
                add_tool(*args)
                return
            except Exception:
                continue

        # 最后尝试仅传入 ID
        try:
            add_tool(tool_id)
        except Exception:
            # 无法注册时静默失败以保证健壮性
            pass

    def _safe_make_property_list(self, PropertyList):
        try:
            return PropertyList()
        except Exception:
            try:
                return PropertyList([])
            except Exception:
                # 退化为普通 list
                return []

    def _property_list_add(self, plist, prop):
        try:
            append = getattr(plist, 'append', None)
            if callable(append):
                append(prop)
                return
        except Exception:
            pass
        try:
            add = getattr(plist, 'add', None)
            if callable(add):
                add(prop)
                return
        except Exception:
            pass
        # 退化为 python list
        try:
            plist += [prop]
        except Exception:
            pass

    def _clone_property_list(self, plist, PropertyList):
        # 尝试创建新实例并复制
        try:
            new_plist = self._safe_make_property_list(PropertyList)
            # 尝试遍历并添加
            try:
                for p in plist:
                    self._property_list_add(new_plist, p)
            except TypeError:
                pass
            return new_plist
        except Exception:
            return plist

    def _get_property_type(self, PropertyType, candidates):
        for name in candidates:
            try:
                if hasattr(PropertyType, name):
                    return getattr(PropertyType, name)
            except Exception:
                continue
        # 尝试获取任意一个类型作为兜底
        try:
            attrs = [a for a in dir(PropertyType) if a.isupper()]
            if attrs:
                return getattr(PropertyType, attrs[0])
        except Exception:
            pass
        return None

    def _make_property(self, Property, PropertyType, name, label, ptype, required=False, default=None, options=None):
        options = options or []
        # 按常见签名尝试构造
        candidates = [
            # 常见关键字签名
            {'name': name, 'label': label, 'type': ptype,
                'required': required, 'default': default, 'options': options},
            {'key': name, 'title': label, 'type': ptype,
                'required': required, 'default': default, 'choices': options},
            {'field': name, 'title': label, 'ptype': ptype,
                'required': required, 'default': default, 'values': options},
            # 常见位置签名
            (name, label, ptype, required, default, options),
            (name, label, ptype),
        ]

        for cand in candidates:
            try:
                if isinstance(cand, dict):
                    return Property(**{k: v for k, v in cand.items() if v is not None})
                else:
                    return Property(*cand)
            except Exception:
                continue

        # 兜底用简单字典表示属性
        return {
            'name': name,
            'label': label,
            'type': getattr(ptype, 'name', str(ptype)) if ptype is not None else 'STRING',
            'required': required,
            'default': default,
            'options': options,
        }
