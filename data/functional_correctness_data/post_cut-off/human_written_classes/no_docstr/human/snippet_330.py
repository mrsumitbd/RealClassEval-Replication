from module.base.timer import Timer

class Product:

    def __init__(self, name, count, button):
        self.name = name
        self.timer = Timer(0, count=count - 1).start()
        self.button: Button = button

    def __str__(self):
        return f'Product: ({self.name}, count: {self.timer.count + 1})'