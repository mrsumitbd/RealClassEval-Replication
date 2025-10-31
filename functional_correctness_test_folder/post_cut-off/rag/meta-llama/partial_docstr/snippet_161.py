
from .tools import GanZhiTool, ShiErChangShengTool, ShiErDiShaTool, NaYinTool, KongWangTool, ShenShaTool, WuXingTool


class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        self.tools['ganzhi'] = add_tool(
            GanZhiTool(PropertyList, Property, PropertyType))
        self.tools['shierchangsheng'] = add_tool(
            ShiErChangShengTool(PropertyList, Property, PropertyType))
        self.tools['shierdisha'] = add_tool(
            ShiErDiShaTool(PropertyList, Property, PropertyType))
        self.tools['naying'] = add_tool(
            NaYinTool(PropertyList, Property, PropertyType))
        self.tools['kongwang'] = add_tool(
            KongWangTool(PropertyList, Property, PropertyType))
        self.tools['shensha'] = add_tool(
            ShenShaTool(PropertyList, Property, PropertyType))
        self.tools['wuxing'] = add_tool(
            WuXingTool(PropertyList, Property, PropertyType))
