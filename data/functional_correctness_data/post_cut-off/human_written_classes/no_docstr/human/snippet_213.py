class Streamer_basic:

    def __init__(self, args, bot_name):
        self.all_text = ''
        self.args = args
        self.bot_name = bot_name

    def __enter__(self):
        print()
        print(col_bot + self.bot_name + ': ' + col_default, end='')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.all_text.endswith('\n'):
            print()

    def stream(self, text: str, think_tag, end_think_tag):
        if self.all_text or not text.startswith(' '):
            print_text = text
        else:
            print_text = text[1:]
        self.all_text += text
        print(print_text, end='', flush=True)