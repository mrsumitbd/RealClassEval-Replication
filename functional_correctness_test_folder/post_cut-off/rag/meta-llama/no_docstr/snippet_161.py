
from .tools import (
    BaZiYearColumnTool,
    BaZiMonthColumnTool,
    BaZiDayColumnTool,
    BaZiTimeColumnTool,
    BaZiSiZhuTool,
    BaZiNaYinTool,
    BaZiWuXingTool,
    BaZiShiShenTool,
    BaZiTenGodTool,
    BaZiTwelveHeavenlyStemTool,
    BaZiShiShenNaYinTool,
    BaZiRelationTool,
    BaZiSeasonTool,
    BaZiDiShiTool,
    BaZiXiangShengTool,
    BaZiXiangKeTool,
    BaZiWangShuaiTool,
    BaZiZhuShouTool,
    BaZiYongShenTool,
    BaZiXiShenTool,
    BaZiNaYinRelationTool,
    BaZiTenGodRelationTool,
)


class BaziManager:
    '''
    八字命理管理器。
    '''

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = []

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        self.tools.append(add_tool(BaZiYearColumnTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiMonthColumnTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiDayColumnTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiTimeColumnTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiSiZhuTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiNaYinTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiWuXingTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiShiShenTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiTenGodTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiTwelveHeavenlyStemTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiShiShenNaYinTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiRelationTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiSeasonTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiDiShiTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiXiangShengTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiXiangKeTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiWangShuaiTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiZhuShouTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiYongShenTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiXiShenTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiNaYinRelationTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiTenGodRelationTool(
            PropertyList, Property, PropertyType)))
