class Plugin:

    def __init__(self, name, module_path, class_name):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self._class = None

    def getClass(self):
        if self._class is None:
            module = __import__(self.module_path, globals(), locals(), [''])
            self._class = getattr(module, self.class_name)
        return self._class