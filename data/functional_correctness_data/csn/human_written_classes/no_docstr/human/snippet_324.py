from inquirer.render.console import ConsoleRender

class Render:

    def __init__(self, impl=ConsoleRender):
        self._impl = impl

    def render(self, question, answers):
        return self._impl.render(question, answers)