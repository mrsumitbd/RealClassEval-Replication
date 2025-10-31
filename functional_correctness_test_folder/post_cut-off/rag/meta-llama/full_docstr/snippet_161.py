
from .tools import (
    BaZiYearColumnTool, BaZiMonthColumnTool, BaZiDayColumnTool, BaZiTimeColumnTool,
    BaZiSiHuaTool, BaZiNaYinTool, BaZiWangShuaiTool, BaZiShiShengTool,
    BaZiShiShenRelationTool, BaZiTenGodTool, BaZiWuXingTool, BaZiShiShenTool
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
        self.tools.append(add_tool(BaZiSiHuaTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiNaYinTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiWangShuaiTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiShiShengTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiShiShenRelationTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiTenGodTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiWuXingTool(
            PropertyList, Property, PropertyType)))
        self.tools.append(add_tool(BaZiShiShenTool(
            PropertyList, Property, PropertyType)))
