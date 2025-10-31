class Streamer_rich:

    def __init__(self, args, bot_name):
        self.all_text = ''
        self.think_text = ''
        self.bot_name = bot_name
        self.all_print_text = col_bot + self.bot_name + col_default + ': '
        self.args = args
        self.live = None
        self.is_live = False

    def begin(self):
        self.live = MarkdownConsoleStream()
        self.live.__enter__()
        self.live.update(self.all_print_text)
        self.is_live = True

    def __enter__(self):
        if self.args.think:
            print()
            print(col_think1 + 'Thinking' + col_default + ': ' + col_think2, end='')
        else:
            print()
            self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.is_live:
            self.live.__exit__(exc_type, exc_value, traceback)

    def stream(self, text: str, think_tag: str, end_think_tag: str):
        if self.args.think and (not self.is_live):
            print_text = text
            if not self.think_text:
                print_text = print_text.lstrip()
            self.think_text += print_text
            if end_think_tag in self.think_text:
                print(print_text.rstrip(), flush=True)
                print()
                self.begin()
            else:
                print(print_text, end='', flush=True)
        else:
            print_text = text
            if not self.all_text.strip():
                print_text = print_text.lstrip()
                if print_text.startswith('```'):
                    print_text = '\n' + print_text
            self.all_text += text
            self.all_print_text += print_text
            formatted_text = self.all_print_text
            formatted_text = formatted_text.replace(think_tag, f'`{think_tag}`')
            formatted_text = formatted_text.replace(end_think_tag, f'`{end_think_tag}`')
            self.live.update(formatted_text)