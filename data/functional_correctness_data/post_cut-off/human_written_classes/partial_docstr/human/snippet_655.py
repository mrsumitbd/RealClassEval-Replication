from collections.abc import Callable

class ConfigMigrationRegistry:

    def __init__(self):
        self._migrations: dict[int, Callable[[dict], dict]] = {}

    def register(self, from_version: int, func: Callable[[dict], dict]) -> None:
        self._migrations[from_version] = func

    def migrate(self, data: dict, current_version: int, target_version: int) -> dict:
        """
        顺序执行 from_version -> from_version+1 ... 直到 target_version
        若中间缺失迁移函数则抛出异常。
        """
        version = current_version
        while version < target_version:
            if version not in self._migrations:
                raise MigrationError(f'Missing migration function for version {version} -> {version + 1}')
            data = self._migrations[version](data)
            version += 1
        return data