from typing import Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type, TypeVar, Union, cast, overload
from django.urls import URLPattern, URLResolver, re_path, reverse, reverse_lazy
from django.utils.safestring import SafeText, mark_safe

class ViewTool:

    def __init__(self, text: str, link: str, perm: Optional[str]=None, **attrs: Any) -> None:
        self.text = text
        self._link = link
        self.perm = perm
        html_class = attrs.pop('html_class', None)
        if html_class is not None:
            attrs.setdefault('class', html_class)
        self._attrs = attrs

    @property
    def attrs(self) -> SafeText:
        return mark_safe(' '.join((f'{k}={v}' for k, v in self._attrs.items())))

    @property
    def link(self) -> str:
        if '/' not in self._link:
            return reverse(self._link)
        return self._link