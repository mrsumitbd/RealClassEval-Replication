from typing import List, Union

class Parse:

    def __init__(self, model: str='th') -> None:
        if model is None:
            model = 'th'
        self.nlp = esupar.load(model)

    def __call__(self, text: str, tag: str='str') -> Union[List[List[str]], str]:
        _data = str(self.nlp(text))
        if tag == 'list':
            _temp = _data.splitlines()
            _tag_data = []
            for i in _temp:
                _tag_data.append(i.split())
            return _tag_data
        return _data