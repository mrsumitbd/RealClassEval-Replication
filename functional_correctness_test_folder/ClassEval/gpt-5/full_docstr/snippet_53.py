from typing import List
import string

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize


class Lemmatization:
    """
    This is a class about Lemmatization, which utilizes the nltk library to perform lemmatization and part-of-speech tagging on sentences, as well as remove punctuation.
    """

    def __init__(self):
        """
        creates a WordNetLemmatizer object and stores it in the self.lemmatizer member variable.
        """
        self.lemmatizer = WordNetLemmatizer()

    def _to_wordnet_pos(self, treebank_tag: str):
        if not treebank_tag:
            return None
        if treebank_tag.startswith('J'):
            return wn.ADJ
        if treebank_tag.startswith('V'):
            return wn.VERB
        if treebank_tag.startswith('N'):
            return wn.NOUN
        if treebank_tag.startswith('R'):
            return wn.ADV
        return None

    def lemmatize_sentence(self, sentence):
        """
        Remove punctuations of the sentence and tokenizes the input sentence, mark the part of speech tag of each word,
        lemmatizes the words with different parameters based on their parts of speech, and stores in a list.
        :param sentence: a sentence str
        :return: a list of words which have been lemmatized.
        >>> lemmatization = Lemmatization()
        >>> lemmatization.lemmatize_sentence("I am running in a race.")
        ['I', 'be', 'run', 'in', 'a', 'race']

        """
        clean = self.remove_punctuation(sentence)
        tokens = word_tokenize(clean)
        tagged = pos_tag(tokens)
        lemmas: List[str] = []
        for token, tag in tagged:
            wn_pos = self._to_wordnet_pos(tag)
            if wn_pos:
                lemmas.append(self.lemmatizer.lemmatize(token, pos=wn_pos))
            else:
                lemmas.append(self.lemmatizer.lemmatize(token))
        return lemmas

    def get_pos_tag(self, sentence):
        """
        Remove punctuations of the sentence and tokenizes the input sentence, mark the part of speech tag of each word.
        :param sentence: a sentence str
        :return: list, part of speech tag of each word in the sentence.
        >>> lemmatization = Lemmatization()
        >>> lemmatization.get_pos_tag("I am running in a race.")
        ['PRP', 'VBP', 'VBG', 'IN', 'DT', 'NN']

        """
        clean = self.remove_punctuation(sentence)
        tokens = word_tokenize(clean)
        tagged = pos_tag(tokens)
        return [tag for _, tag in tagged]

    def remove_punctuation(self, sentence):
        """
        Removes punctuation from the input text.
        :param sentence: a sentence str
        :return: str, sentence without any punctuation
        >>> lemmatization = Lemmatization()
        >>> lemmatization.remove_punctuation("I am running in a race.")
        'I am running in a race'

        """
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)
