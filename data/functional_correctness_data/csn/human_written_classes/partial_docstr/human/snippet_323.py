import warnings
from pythainlp.tokenize import word_tokenize
from typing import List, Tuple, Union

class NamedEntityRecognition:

    def __init__(self, model: str='pythainlp/thainer-corpus-v2-base-model') -> None:
        """
        This function tags named entities in text in IOB format.

        Powered by wangchanberta from VISTEC-depa             AI Research Institute of Thailand
        :param str model: The model that use wangchanberta pretrained.
        """
        from transformers import AutoModelForTokenClassification, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForTokenClassification.from_pretrained(model)

    def _fix_span_error(self, words, ner):
        _ner = []
        _ner = ner
        _new_tag = []
        for i, j in zip(words, _ner):
            i = self.tokenizer.decode(i)
            if i.isspace() and j.startswith('B-'):
                j = 'O'
            if i in ('', '<s>', '</s>'):
                continue
            if i == '<_>':
                i = ' '
            _new_tag.append((i, j))
        return _new_tag

    def get_ner(self, text: str, pos: bool=False, tag: bool=False) -> Union[List[Tuple[str, str]], str]:
        """
        This function tags named entities in text in IOB format.
        Powered by wangchanberta from VISTEC-depa             AI Research Institute of Thailand

        :param str text: text in Thai to be tagged
        :param bool tag: output HTML-like tags.
        :return: a list of tuples associated with tokenized word groups, NER tags,                  and output HTML-like tags (if the parameter `tag` is                  specified as `True`).                  Otherwise, return a list of tuples associated with tokenized                  words and NER tags
        :rtype: Union[list[tuple[str, str]]], str
        """
        import torch
        if pos:
            warnings.warn("This model doesn't support output postag and It doesn't output the postag.")
        words_token = word_tokenize(text.replace(' ', '<_>'))
        inputs = self.tokenizer(words_token, is_split_into_words=True, return_tensors='pt')
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        outputs = self.model(ids, attention_mask=mask)
        logits = outputs[0]
        predictions = torch.argmax(logits, dim=2)
        predicted_token_class = [self.model.config.id2label[t.item()] for t in predictions[0]]
        ner_tag = self._fix_span_error(inputs['input_ids'][0], predicted_token_class)
        if tag:
            temp = ''
            sent = ''
            for idx, (word, ner) in enumerate(ner_tag):
                if ner.startswith('B-') and temp != '':
                    sent += '</' + temp + '>'
                    temp = ner[2:]
                    sent += '<' + temp + '>'
                elif ner.startswith('B-'):
                    temp = ner[2:]
                    sent += '<' + temp + '>'
                elif ner == 'O' and temp != '':
                    sent += '</' + temp + '>'
                    temp = ''
                sent += word
                if idx == len(ner_tag) - 1 and temp != '':
                    sent += '</' + temp + '>'
            return sent
        return ner_tag