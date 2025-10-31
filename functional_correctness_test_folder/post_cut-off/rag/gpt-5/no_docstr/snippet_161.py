class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self._registered = False
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        if self._registered:
            return

        def _ptype(name, fallback=None):
            candidates = [name, name.upper(), name.lower(), name.capitalize()]
            for cand in candidates:
                if hasattr(PropertyType, cand):
                    return getattr(PropertyType, cand)
            return fallback if fallback is not None else name.lower()

        def _make_property(key, label, ptype, required=True, default=None, options=None, description=None):
            kwargs = {
                'key': key,
                'label': label,
                'type': ptype,
                'required': required,
            }
            if default is not None:
                kwargs['default'] = default
            if options is not None:
                kwargs['options'] = options
            if description is not None:
                kwargs['description'] = description
            try:
                return Property(**kwargs)
            except Exception:
                # Fallback to plain dict
                return kwargs

        def _make_property_list(props):
            try:
                return PropertyList(props)
            except Exception:
                return list(props)

        def _safe_add_tool(tool):
            # Try multiple common signatures to register tools
            try:
                add_tool(tool)
                return
            except TypeError:
                pass
            try:
                add_tool(tool.get('id'), tool.get('properties'))
                return
            except TypeError:
                pass
            try:
                add_tool(tool.get('id'), tool.get(
                    'name'), tool.get('properties'))
                return
            except TypeError:
                pass
            # Final generic attempt
            add_tool(tool)

        # Common property types
        PT_STRING = _ptype('STRING')
        PT_DATE = _ptype('DATE')
        PT_TIME = _ptype('TIME')
        PT_ENUM = _ptype('ENUM')
        PT_BOOLEAN = _ptype('BOOLEAN')
        PT_INTEGER = _ptype('INTEGER', fallback=_ptype(
            'NUMBER', fallback='number'))

        # Tool 1: 八字排盘
        chart_props = _make_property_list([
            _make_property('birth_date', '出生日期', PT_DATE,
                           required=True, description='公历出生日期'),
            _make_property('birth_time', '出生时间', PT_TIME,
                           required=False, description='出生具体时间（可选）'),
            _make_property('gender', '性别', PT_ENUM, required=True, default='male', options=[
                {'value': 'male', 'label': '男'},
                {'value': 'female', 'label': '女'},
            ]),
            _make_property('calendar', '历法', PT_ENUM, required=True, default='solar', options=[
                {'value': 'solar', 'label': '公历'},
                {'value': 'lunar', 'label': '农历'},
            ]),
            _make_property('timezone', '时区', PT_STRING, required=False,
                           description='时区，例如 Asia/Shanghai 或 +08:00'),
        ])
        chart_tool = {
            'id': 'bazi.chart',
            'name': '八字排盘',
            'properties': chart_props,
        }
        _safe_add_tool(chart_tool)
        self.tools[chart_tool['id']] = chart_tool

        # Tool 2: 合婚（两人八字合婚）
        match_props = _make_property_list([
            _make_property('p1_birth_date', '甲方出生日期', PT_DATE, required=True),
            _make_property('p1_birth_time', '甲方出生时间', PT_TIME, required=False),
            _make_property('p1_gender', '甲方性别', PT_ENUM, required=True, default='male', options=[
                {'value': 'male', 'label': '男'},
                {'value': 'female', 'label': '女'},
            ]),

            _make_property('p2_birth_date', '乙方出生日期', PT_DATE, required=True),
            _make_property('p2_birth_time', '乙方出生时间', PT_TIME, required=False),
            _make_property('p2_gender', '乙方性别', PT_ENUM, required=True, default='female', options=[
                {'value': 'male', 'label': '男'},
                {'value': 'female', 'label': '女'},
            ]),

            _make_property('calendar', '历法', PT_ENUM, required=True, default='solar', options=[
                {'value': 'solar', 'label': '公历'},
                {'value': 'lunar', 'label': '农历'},
            ]),
            _make_property('timezone', '时区', PT_STRING, required=False),
        ])
        match_tool = {
            'id': 'bazi.compatibility',
            'name': '八字合婚',
            'properties': match_props,
        }
        _safe_add_tool(match_tool)
        self.tools[match_tool['id']] = match_tool

        # Tool 3: 流年运势（指定年份）
        transit_props = _make_property_list([
            _make_property('birth_date', '出生日期', PT_DATE, required=True),
            _make_property('birth_time', '出生时间', PT_TIME, required=False),
            _make_property('gender', '性别', PT_ENUM, required=True, default='male', options=[
                {'value': 'male', 'label': '男'},
                {'value': 'female', 'label': '女'},
            ]),
            _make_property('year', '年份', PT_INTEGER,
                           required=True, description='需查询的公历年份'),
            _make_property('calendar', '历法', PT_ENUM, required=True, default='solar', options=[
                {'value': 'solar', 'label': '公历'},
                {'value': 'lunar', 'label': '农历'},
            ]),
            _make_property('timezone', '时区', PT_STRING, required=False),
        ])
        transit_tool = {
            'id': 'bazi.transit',
            'name': '流年运势',
            'properties': transit_props,
        }
        _safe_add_tool(transit_tool)
        self.tools[transit_tool['id']] = transit_tool

        self._registered = True
