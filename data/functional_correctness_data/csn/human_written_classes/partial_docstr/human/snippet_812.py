from jinja2 import Template

class _LinearColormaps:
    """A class for hosting the list of built-in linear colormaps."""

    def __init__(self):
        self._schemes = _schemes.copy()
        self._colormaps = {key: LinearColormap(val) for key, val in _schemes.items()}
        for key, val in _schemes.items():
            setattr(self, key, LinearColormap(val))

    def _repr_html_(self) -> str:
        return Template('\n        <table>\n        {% for key,val in this._colormaps.items() %}\n        <tr><td>{{key}}</td><td>{{val._repr_html_()}}</td></tr>\n        {% endfor %}</table>\n        ').render(this=self)