from module.logger import HTMLConsole, Highlighter, WEB_THEME
from module.webui.process_manager import ProcessManager
from pywebio.session import eval_js, local, run_js
from module.webui.utils import DARK_TERMINAL_THEME, LIGHT_TERMINAL_THEME, LOG_CODE_FORMAT, Switch
from rich.console import ConsoleRenderable
from typing import Any, Callable, Dict, Generator, List, Optional, TYPE_CHECKING, Union
from pywebio.exceptions import SessionException
from module.webui.setting import State

class RichLog:

    def __init__(self, scope, font_width='0.559') -> None:
        self.scope = scope
        self.font_width = font_width
        self.console = HTMLConsole(force_terminal=False, force_interactive=False, width=80, color_system='truecolor', markup=False, record=True, safe_box=False, highlighter=Highlighter(), theme=WEB_THEME)
        self.keep_bottom = True
        if State.theme == 'dark':
            self.terminal_theme = DARK_TERMINAL_THEME
        else:
            self.terminal_theme = LIGHT_TERMINAL_THEME

    def render(self, renderable: ConsoleRenderable) -> str:
        with self.console.capture():
            self.console.print(renderable)
        html = self.console.export_html(theme=self.terminal_theme, clear=True, code_format=LOG_CODE_FORMAT, inline_styles=True)
        return html

    def extend(self, text):
        if text:
            run_js('$("#pywebio-scope-{scope}>div").append(text);\n            '.format(scope=self.scope), text=str(text))
            if self.keep_bottom:
                self.scroll()

    def reset(self):
        run_js(f'$("#pywebio-scope-{self.scope}>div").empty();')

    def scroll(self) -> None:
        run_js('$("#pywebio-scope-{scope}").scrollTop($("#pywebio-scope-{scope}").prop("scrollHeight"));\n        '.format(scope=self.scope))

    def set_scroll(self, b: bool) -> None:
        self.keep_bottom = b

    def get_width(self):
        js = '\n        let canvas = document.createElement(\'canvas\');\n        canvas.style.position = "absolute";\n        let ctx = canvas.getContext(\'2d\');\n        document.body.appendChild(canvas);\n        ctx.font = `16px Menlo, consolas, DejaVu Sans Mono, Courier New, monospace`;\n        document.body.removeChild(canvas);\n        let text = ctx.measureText(\'0\');\n        ctx.fillText(\'0\', 50, 50);\n\n        ($(\'#pywebio-scope-{scope}\').width()-16)/        $(\'#pywebio-scope-{scope}\').css(\'font-size\').slice(0, -2)/text.width*16;        '.format(scope=self.scope)
        width = eval_js(js)
        return 80 if width is None else 128 if width > 128 else int(width)

    def put_log(self, pm: ProcessManager) -> Generator:
        yield
        try:
            while True:
                last_idx = len(pm.renderables)
                html = ''.join(map(self.render, pm.renderables[:]))
                self.reset()
                self.extend(html)
                counter = last_idx
                while counter < pm.renderables_max_length * 2:
                    yield
                    idx = len(pm.renderables)
                    if idx < last_idx:
                        last_idx -= pm.renderables_reduce_length
                    if idx != last_idx:
                        html = ''.join(map(self.render, pm.renderables[last_idx:idx]))
                        self.extend(html)
                        counter += idx - last_idx
                        last_idx = idx
        except SessionException:
            pass