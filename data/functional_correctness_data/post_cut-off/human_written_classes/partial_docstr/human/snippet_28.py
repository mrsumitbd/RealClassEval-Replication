class DeviceTypeRegistry:
    """设备类型注册表，用于管理IOT设备类型及其函数"""

    def __init__(self):
        self.type_functions = {}

    def generate_device_type_id(self, descriptor):
        """通过设备能力描述生成类型ID"""
        properties = sorted(descriptor['properties'].keys())
        methods = sorted(descriptor['methods'].keys())
        type_signature = f"{descriptor['name']}:{','.join(properties)}:{','.join(methods)}"
        return type_signature

    def get_device_functions(self, type_id):
        """获取设备类型对应的所有函数"""
        return self.type_functions.get(type_id, {})

    def register_device_type(self, type_id, functions):
        """注册设备类型及其函数"""
        if type_id not in self.type_functions:
            self.type_functions[type_id] = functions