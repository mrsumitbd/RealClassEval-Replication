import warnings
from typing import Callable, List, Tuple, Union

class NamedEntityTagger:

    def __init__(self, model: str='Pavarissy/phayathaibert-thainer') -> None:
        from transformers import AutoModelForTokenClassification, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def get_ner(self, text: str, tag: bool=False, pos: bool=False, strategy: str='simple') -> Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]:
        """
        This function tags named entities in text in IOB format.

        :param str text: text in Thai to be tagged
        :param bool pos: output with part-of-speech tags.            (PhayaThaiBERT is supported in PartOfSpeechTagger)
        :return: a list of tuples associated with tokenized words, NER tags,
                 POS tags (if the parameter `pos` is specified as `True`),
                 and output HTML-like tags (if the parameter `tag` is
                 specified as `True`).
                 Otherwise, return a list of tuples associated with tokenized
                 words and NER tags
        :rtype: Union[List[Tuple[str, str]], List[Tuple[str, str, str]], str]
        :Example:

            >>> from pythainlp.phayathaibert.core import NamedEntityTagger
            >>>
            >>> tagger = NamedEntityTagger()
            >>> tagger.get_ner("ทดสอบนายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย")
            [('นายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย', 'PERSON'),
            ('จาก', 'LOCATION'),
            ('ประเทศไทย', 'LOCATION')]
            >>> ner.tag("ทดสอบนายปวริศ เรืองจุติโพธิ์พานจากประเทศไทย", tag=True)
            'ทดสอบ<PERSON>นายปวริศ เรืองจุติโพธิ์พาน</PERSON>                <LOCATION>จาก</LOCATION><LOCATION>ประเทศไทย</LOCATION>'
        """
        from transformers import TokenClassificationPipeline
        if pos:
            warnings.warn("This model doesn't support output                           postag and It doesn't output the postag.")
        sample_output = []
        tag_text_list = []
        current_pos = 0
        pipeline = TokenClassificationPipeline(model=self.model, tokenizer=self.tokenizer, aggregation_strategy=strategy)
        outputs = pipeline(text)
        for token in outputs:
            ner_tag = token['entity_group']
            begin_pos, end_pos = (token['start'], token['end'])
            if current_pos == 0:
                text_tag = text[:begin_pos] + f'<{ner_tag}>' + text[begin_pos:end_pos] + f'</{ner_tag}>'
            else:
                text_tag = text[current_pos:begin_pos] + f'<{ner_tag}>' + text[begin_pos:end_pos] + f'</{ner_tag}>'
            tag_text_list.append(text_tag)
            sample_output.append((token['word'], token['entity_group']))
            current_pos = end_pos
        if tag:
            return str(''.join(tag_text_list))
        return sample_output