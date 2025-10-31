from typing import Optional, Union, Tuple, Callable, Dict, Sequence, Any
from borax.calendars.festivals2 import FestivalLibrary, WrappedDate, Festival

class FestivalItemAdapter:
    """A helper class for display list data."""
    FIELDS = {'name': '名称', 'description': '描述', 'code': '编码', 'next_day': '下一个日期', 'countdown': '倒计天数'}

    def __init__(self, columns: Sequence):
        self.fields = []
        self.displays = []
        self.widths = []
        for cfg in columns:
            if isinstance(cfg, (list, tuple)):
                _f, _w = cfg
            else:
                _f, _w = (cfg, 200)
            self.fields.append(_f)
            self.displays.append(FestivalItemAdapter.FIELDS.get(_f))
            self.widths.append(_w)

    def object2values(self, festival: Festival, wd: WrappedDate=None, ndays: int=0):
        obj_dic = {'code': festival.encode(), 'name': festival.name, 'description': festival.description, 'catalog': festival.catalog}
        if wd is None:
            ndays, wd = festival.countdown()
        obj_dic.update({'next_day': wd.simple_str(), 'countdown': str(ndays)})
        return [obj_dic.get(_f) for _f in self.fields]