class BaziManager:

    def __init__(self):
        self._tools = {}
        self._add_tool = None
        self._PropertyList = None
        self._Property = None
        self._PropertyType = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        import inspect

        self._add_tool = add_tool
        self._PropertyList = PropertyList
        self._Property = Property
        self._PropertyType = PropertyType

        def bazi_echo(**kwargs):
            return {"echo": kwargs}

        self._tools["bazi_echo"] = bazi_echo

        sig = inspect.signature(add_tool)
        params = list(sig.parameters.values())
        param_names = [p.name for p in params]

        called = False
        try:
            add_tool(bazi_echo)
            called = True
        except Exception:
            pass

        if not called:
            try:
                if {"name", "func"}.issubset(param_names):
                    add_tool(name="bazi_echo", func=bazi_echo)
                    called = True
            except Exception:
                pass

        if not called:
            try:
                if {"name", "function"}.issubset(param_names):
                    add_tool(name="bazi_echo", function=bazi_echo)
                    called = True
            except Exception:
                pass

        if not called:
            try:
                if len(params) == 2:
                    add_tool(bazi_echo, "bazi_echo")
                    called = True
            except Exception:
                pass

        if not called:
            try:
                add_tool(tool=bazi_echo)
                called = True
            except Exception:
                pass

        return {"registered": "bazi_echo", "success": called}
