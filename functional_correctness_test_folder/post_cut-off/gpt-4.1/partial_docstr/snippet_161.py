
class BaziManager:

    def __init__(self):
        '''
        初始化八字管理器.
        '''
        self.tools = []
        self.PropertyList = None
        self.Property = None
        self.PropertyType = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        '''
        初始化并注册所有八字命理工具。
        '''
        self.PropertyList = PropertyList
        self.Property = Property
        self.PropertyType = PropertyType

        # 假设有一些八字命理工具类，这里用字符串代替
        tool_names = [
            "HeavenlyStemsTool",
            "EarthlyBranchesTool",
            "FiveElementsTool",
            "TenGodsTool",
            "LuckCycleTool"
        ]
        for tool_name in tool_names:
            tool = add_tool(tool_name)
            self.tools.append(tool)
