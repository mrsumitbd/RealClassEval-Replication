
from typing import List, Tuple
import random


class FastTextAug:
    '''
    Text Augment from fastText
    :param str model_path: path of model file
    '''

    def __init__(self, model_path: str):
        '''
        :param str model_path: path of model file
        '''
        import fasttext
        self.model = fasttext.load_model(model_path)

    def tokenize(self, text: str) -> List[str]:
        '''
        Thai text tokenization for fastText
        :param str text: Thai text
        :return: list of words
        :rtype: List[str]
        '''
        # Simple whitespace tokenization; for Thai, you may want to use a better tokenizer
        return text.strip().split()

    def modify_sent(self, sent: str, p: float = 0.7) -> List[List[str]]:
        '''
        :param str sent: text of sentence
        :param float p: probability
        :rtype: List[List[str]]
        '''
        words = self.tokenize(sent)
        aug_sents = []
        for i, word in enumerate(words):
            if random.random() < p:
                # Get top 5 nearest neighbors
                try:
                    neighbors = self.model.get_nearest_neighbors(word)
                except Exception:
                    neighbors = []
                synonyms = [w for _, w in neighbors if w != word]
                if synonyms:
                    for syn in synonyms[:3]:  # limit to 3 synonyms per word
                        new_words = words.copy()
                        new_words[i] = syn
                        aug_sents.append(new_words)
        return aug_sents if aug_sents else [words]

    def augment(self, sentence: str, n_sent: int = 1, p: float = 0.7) -> List[Tuple[str]]:
        '''
        Text Augment from fastText
        You may want to download the Thai model
        from https://fasttext.cc/docs/en/crawl-vectors.html.
        :param str sentence: Thai sentence
        :param int n_sent: number of sentences
        :param float p: probability of word
        :return: list of synonyms
        :rtype: List[Tuple[str]]
        '''
        augmented = set()
        tries = 0
        max_tries = n_sent * 10
        while len(augmented) < n_sent and tries < max_tries:
            aug_sents = self.modify_sent(sentence, p)
            for aug in aug_sents:
                aug_text = ' '.join(aug)
                if aug_text != sentence:
                    augmented.add(tuple([aug_text]))
                if len(augmented) >= n_sent:
                    break
            tries += 1
        if not augmented:
            return [(sentence,)]
        return list(augmented)[:n_sent]
