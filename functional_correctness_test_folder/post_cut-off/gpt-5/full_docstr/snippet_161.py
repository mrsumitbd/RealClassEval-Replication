class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self._registered = []
        self._meta = []

    def _build_property(self, Property, PropertyType, name, ptype, description='', required=False, enum=None, default=None):
        prop = None
        # Try common constructor signatures
        tried = []
        for ctor in (
            lambda: Property(name, ptype, description,
                             required, enum, default),
            lambda: Property(name=name, type=ptype, description=description,
                             required=required, enum=enum, default=default),
            lambda: Property(name=name, ptype=ptype, desc=description,
                             required=required, enum=enum, default=default),
            lambda: Property(),
        ):
            try:
                prop = ctor()
                break
            except Exception as e:
                tried.append(e)
                prop = None
        # Fallback to simple object-like dict if instantiation failed
        if prop is None:
            return {
                'name': name,
                'type': ptype if isinstance(ptype, str) else str(ptype),
                'description': description,
                'required': bool(required),
                'enum': list(enum) if enum else None,
                'default': default,
            }
        # Try attribute assignments to cover various schemas
        for key, val in (
            ('name', name),
            ('key', name),
            ('field', name),
            ('type', ptype),
            ('ptype', ptype),
            ('data_type', ptype),
            ('description', description),
            ('desc', description),
            ('required', bool(required)),
            ('is_required', bool(required)),
            ('enum', list(enum) if enum else None),
            ('choices', list(enum) if enum else None),
            ('default', default),
            ('default_value', default),
        ):
            try:
                setattr(prop, key, val)
            except Exception:
                pass
        return prop

    def _build_property_list(self, PropertyList, props):
        # Try to initialize PropertyList with iterable
        try:
            return PropertyList(props)
        except Exception:
            pass
        # Try empty init then extend
        try:
            pl = PropertyList()
            # Try common extension patterns
            try:
                pl.extend(props)  # list-like
                return pl
            except Exception:
                pass
            try:
                for p in props:
                    pl.add(p)
                return pl
            except Exception:
                pass
            try:
                for p in props:
                    pl.append(p)
                return pl
            except Exception:
                pass
            return pl
        except Exception:
            # Fallback to simple list
            return list(props)

    def _try_add_tool(self, add_tool, tool_payload):
        # Try various calling conventions for add_tool
        name = tool_payload.get('name')
        description = tool_payload.get('description')
        properties = tool_payload.get('properties')
        # 1) name, description, properties
        try:
            add_tool(name, description, properties)
            return True
        except Exception:
            pass
        # 2) dict payload
        try:
            add_tool(tool_payload)
            return True
        except Exception:
            pass
        # 3) name, payload
        try:
            add_tool(name, tool_payload)
            return True
        except Exception:
            pass
        # 4) description, properties, name (some APIs use different orders)
        try:
            add_tool(description, properties, name)
            return True
        except Exception:
            pass
        return False

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        tools_meta = []

        # 工具一：计算八字（根据公历/农历出生信息）
        props_calc = [
            self._build_property(Property, PropertyType, name='birth_date', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='出生日期，格式YYYY-MM-DD（公历或农历取决于calendar）', required=True),
            self._build_property(Property, PropertyType, name='birth_time', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='出生时间，格式HH:MM，24小时制；未知可传00:00', required=True),
            self._build_property(Property, PropertyType, name='calendar', ptype=getattr(PropertyType, 'Enum', 'string'),
                                 description='历法类型：solar(公历)/lunar(农历)', required=False, enum=['solar', 'lunar'], default='solar'),
            self._build_property(Property, PropertyType, name='timezone', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='时区，IANA格式如Asia/Shanghai；默认Asia/Shanghai', required=False, default='Asia/Shanghai'),
            self._build_property(Property, PropertyType, name='gender', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='性别：male/female/unknown', required=False, enum=['male', 'female', 'unknown'], default='unknown'),
        ]
        tools_meta.append({
            'name': 'calc_bazi',
            'description': '根据出生日期时间计算四柱八字（年柱、月柱、日柱、时柱）及相关信息。',
            'properties': self._build_property_list(PropertyList, props_calc),
        })

        # 工具二：干支转换（公历日期时间 -> 天干地支）
        props_ganzhi = [
            self._build_property(Property, PropertyType, name='year', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='年份（公历）', required=True),
            self._build_property(Property, PropertyType, name='month', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='月份（1-12）', required=True),
            self._build_property(Property, PropertyType, name='day', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='日期（1-31）', required=True),
            self._build_property(Property, PropertyType, name='hour', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='小时（0-23）', required=False, default=0),
            self._build_property(Property, PropertyType, name='minute', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='分钟（0-59）', required=False, default=0),
            self._build_property(Property, PropertyType, name='timezone', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='时区，IANA格式如Asia/Shanghai；默认Asia/Shanghai', required=False, default='Asia/Shanghai'),
        ]
        tools_meta.append({
            'name': 'ganzhi_from_gregorian',
            'description': '将公历日期时间转换为年、月、日、时的天干地支。',
            'properties': self._build_property_list(PropertyList, props_ganzhi),
        })

        # 工具三：八字合盘匹配度
        props_match = [
            self._build_property(Property, PropertyType, name='self_bazi', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='己方八字，格式如“甲子 乙丑 丙寅 丁卯”', required=True),
            self._build_property(Property, PropertyType, name='other_bazi', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='对方八字，格式如“庚辰 辛巳 壬午 癸未”', required=True),
            self._build_property(Property, PropertyType, name='focus', ptype=getattr(PropertyType, 'Enum', 'string'),
                                 description='匹配侧重点：overall/affection/career/wealth/health', required=False,
                                 enum=['overall', 'affection', 'career', 'wealth', 'health'], default='overall'),
        ]
        tools_meta.append({
            'name': 'bazi_compatibility',
            'description': '根据双方八字进行匹配度评估与要点提示。',
            'properties': self._build_property_list(PropertyList, props_match),
        })

        # 工具四：流年/大运分析输入
        props_fortune = [
            self._build_property(Property, PropertyType, name='bazi', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='基础八字，格式“年柱 月柱 日柱 时柱”', required=True),
            self._build_property(Property, PropertyType, name='year', ptype=getattr(PropertyType, 'Integer', 'integer'),
                                 description='欲分析的年份（公历）', required=True),
            self._build_property(Property, PropertyType, name='gender', ptype=getattr(PropertyType, 'String', 'string'),
                                 description='性别：male/female/unknown（用于起大运）', required=False, enum=['male', 'female', 'unknown'], default='unknown'),
            self._build_property(Property, PropertyType, name='start_from_birth', ptype=getattr(PropertyType, 'Boolean', 'boolean'),
                                 description='大运起运从出生起算（True）或按传统起运法（False）', required=False, default=False),
        ]
        tools_meta.append({
            'name': 'bazi_fortune_trend',
            'description': '基于八字进行指定年份的流年/大运走势分析输入定义。',
            'properties': self._build_property_list(PropertyList, props_fortune),
        })

        # 注册工具
        self._meta = tools_meta
        self._registered = []
        for tool in tools_meta:
            if self._try_add_tool(add_tool, tool):
                self._registered.append(tool.get('name'))
            else:
                # 无法注册时仍记录尝试过的工具名称
                self._registered.append(f"failed:{tool.get('name')}")
