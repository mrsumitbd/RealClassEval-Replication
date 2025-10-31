from dataclasses import dataclass, field

@dataclass
class PythonDependency:
    """Python包依赖信息"""
    package_name: str
    version: str = ''
    optional: bool = False
    description: str = ''
    install_name: str = ''

    def __post_init__(self):
        if not self.install_name:
            self.install_name = self.package_name

    def get_pip_requirement(self) -> str:
        """获取pip安装格式的依赖字符串"""
        if self.version:
            return f'{self.install_name}{self.version}'
        return self.install_name