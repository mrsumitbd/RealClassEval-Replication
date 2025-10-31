from typing import List, Tuple, Union

class NNER:
    """
    Nested Named Entity Recognition

    :param str engine: engine of nested named entity recognizer
    :param str corpus: corpus

    **Options for engine**
        * *thai_nner* - Thai NER engine
    """

    def __init__(self, engine: str='thai_nner') -> None:
        self.load_engine(engine)

    def load_engine(self, engine: str='thai_nner') -> None:
        from pythainlp.tag.thai_nner import Thai_NNER
        self.engine = Thai_NNER()

    def tag(self, text) -> Tuple[List[str], List[dict]]:
        """
        This function tags nested named entities.

        :param str text: text in Thai to be tagged

        :return: a list of tuples associated with tokenized words and NNER tags.
        :rtype: Tuple[List[str], List[dict]]

        :Example:

            >>> from pythainlp.tag.named_entity import NNER
            >>> nner = NNER()
            >>> nner.tag("แมวทำอะไรตอนห้าโมงเช้า")
            ([
                '<s>',
                '',
                'แมว',
                'ทํา',
                '',
                'อะไร',
                'ตอน',
                '',
                'ห้า',
                '',
                'โมง',
                '',
                'เช้า',
                '</s>'
            ],
            [
                {
                    'text': ['', 'ห้า'],
                    'span': [7, 9],
                    'entity_type': 'cardinal'
                },
                {
                    'text': ['', 'ห้า', '', 'โมง'],
                    'span': [7, 11],
                    'entity_type': 'time'
                },
                {
                    'text': ['', 'โมง'],
                    'span': [9, 11],
                    'entity_type': 'unit'
                }
            ])
        """
        return self.engine.tag(text)