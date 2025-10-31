import string
from pywebio.session import eval_js, local, run_js
import random

class ScrollableCode:
    """
    https://github.com/pywebio/PyWebIO/discussions/21
    Deprecated
    """

    def __init__(self, keep_bottom: bool=True) -> None:
        self.keep_bottom = keep_bottom
        self.id = ''.join((random.choice(string.ascii_letters) for _ in range(10)))
        self.html = '<pre id="%s" class="container-log"><code style="white-space:break-spaces;"></code></pre>' % self.id

    def output(self):
        return put_html(self.html)

    def append(self, text: str) -> None:
        if text:
            run_js('$("#{dom_id}>code").append(text);\n            '.format(dom_id=self.id), text=str(text))
            if self.keep_bottom:
                self.scroll()

    def scroll(self) -> None:
        run_js('$("\\#{dom_id}").animate({{scrollTop: $("\\#{dom_id}").prop("scrollHeight")}}, 0);\n        '.format(dom_id=self.id))

    def reset(self) -> None:
        run_js('$("\\#{dom_id}>code").empty();'.format(dom_id=self.id))

    def set_scroll(self, b: bool) -> None:
        self.keep_bottom = b