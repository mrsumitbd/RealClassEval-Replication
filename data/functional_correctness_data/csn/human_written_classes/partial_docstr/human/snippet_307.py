from typing import Callable, List, Tuple, Union

class PartOfSpeechTagger:

    def __init__(self, model: str='lunarlist/pos_thai_phayathai') -> None:
        from transformers import AutoModelForTokenClassification, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def get_tag(self, sentence: str, strategy: str='simple') -> List[List[Tuple[str, str]]]:
        """
        Marks sentences with part-of-speech (POS) tags.

        :param str sentence: a list of lists of tokenized words
        :return: a list of lists of tuples (word, POS tag)
        :rtype: list[list[tuple[str, str]]]

        :Example:

        Labels POS for given sentence::

            from pythainlp.phayathaibert.core import PartOfSpeechTagger

            tagger = PartOfSpeechTagger()
            tagger.get_tag("แมวทำอะไรตอนห้าโมงเช้า")
            # output:
            # [[('แมว', 'NOUN'), ('ทําอะไร', 'VERB'), ('ตอนห้าโมงเช้า', 'NOUN')]]
        """
        from transformers import TokenClassificationPipeline
        pipeline = TokenClassificationPipeline(model=self.model, tokenizer=self.tokenizer, aggregation_strategy=strategy)
        outputs = pipeline(sentence)
        word_tags = [[(tag['word'], tag['entity_group']) for tag in outputs]]
        return word_tags