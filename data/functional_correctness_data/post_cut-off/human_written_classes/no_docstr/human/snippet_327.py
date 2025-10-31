import traceback

class Page:
    parent = None

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        filename, line_number, function_name, text = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button