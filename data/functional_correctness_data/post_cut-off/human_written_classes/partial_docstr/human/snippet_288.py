class DBWrapper:
    """数据库代理类，保持接口兼容性同时实现懒加载。"""

    def __getattr__(self, name):
        return getattr(get_db(), name)

    def __getitem__(self, key):
        return get_db()[key]