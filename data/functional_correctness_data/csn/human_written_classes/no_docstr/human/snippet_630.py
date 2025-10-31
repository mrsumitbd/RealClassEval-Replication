class MockIO:

    def __init__(self):
        self.session = None

    def readline(self, prompt='', add_to_history=False):
        print(prompt)
        return 'quit'

    def output(self):
        print()
    pass