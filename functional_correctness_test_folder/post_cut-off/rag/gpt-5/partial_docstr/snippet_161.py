class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = {}
        self.initialized = False
        self.context = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        if self.initialized:
            return

        # Keep lightweight references to provided types for external usage if needed
        self.context = {
            'PropertyList': PropertyList,
            'Property': Property,
            'PropertyType': PropertyType,
        }

        stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        def list_heavenly_stems():
            return list(stems)

        def list_earthly_branches():
            return list(branches)

        def combine_ganzhi_index(i):
            i = int(i) % 60
            return stems[i % 10] + branches[i % 12]

        def ganzhi_cycle():
            return [combine_ganzhi_index(i) for i in range(60)]

        def year_pillar_from_year(year):
            y = int(year)
            stem = stems[(y - 4) % 10]
            branch = branches[(y - 4) % 12]
            return stem + branch

        def bazi_from_datetime(dt=None, year=None, month=None, day=None, hour=None):
            if dt is not None:
                try:
                    year = getattr(dt, 'year')
                    month = getattr(dt, 'month', None)
                    day = getattr(dt, 'day', None)
                    hour = getattr(dt, 'hour', None)
                except Exception:
                    pass
            if year is None:
                raise ValueError('需要提供年信息（dt 或 year）')

            year_pillar = year_pillar_from_year(year)

            # 简化：仅计算年柱，其余返回 None 以保持 API 稳定
            return {
                'year': year_pillar,
                'month': None,
                'day': None,
                'hour': None,
            }

        def is_yang_stem(stem):
            try:
                idx = stems.index(stem)
            except ValueError:
                return None
            return idx % 2 == 0

        def is_yin_stem(stem):
            r = is_yang_stem(stem)
            return None if r is None else (not r)

        def _register(name, func, description=None):
            self.tools[name] = func
            # Try common add_tool signatures: (name, func, meta), (name, func), ({...})
            meta = {'description': description} if description else None
            try:
                add_tool(name, func, meta=meta)
            except TypeError:
                try:
                    add_tool(name, func)
                except TypeError:
                    payload = {'name': name, 'func': func}
                    if description:
                        payload['description'] = description
                    add_tool(payload)

        _register('天干列表', list_heavenly_stems, '返回十天干序列')
        _register('地支列表', list_earthly_branches, '返回十二地支序列')
        _register('六十甲子', ganzhi_cycle, '返回标准六十甲子序列（从甲子开始）')
        _register('干支序号合成', combine_ganzhi_index, '根据 0-59 序号合成干支')
        _register('年份干支', year_pillar_from_year, '根据公历年份计算年柱（简化版）')
        _register('八字排盘(简)', bazi_from_datetime, '根据日期时间计算简化八字（仅年柱）')
        _register('天干为阳', is_yang_stem, '判断天干阴阳：阳为 True，阴为 False')
        _register('天干为阴', is_yin_stem, '判断天干阴阳：阴为 True，阳为 False')

        self.initialized = True
