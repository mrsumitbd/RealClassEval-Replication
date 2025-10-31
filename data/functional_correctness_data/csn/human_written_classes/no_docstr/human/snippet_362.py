import os
from goose3.utils import FileHelper, deprecated
import re
from typing import Dict, Set
import string

class StopWords:
    _cached_stop_words: Dict[str, Set[str]] = {}

    def __init__(self, language='en'):
        if language not in self._cached_stop_words:
            path = os.path.join('resources', 'text', f'stopwords-{language}.txt')
            try:
                content = FileHelper.load_resource_file(path)
                word_list = content.splitlines()
            except OSError:
                word_list = []
            self._cached_stop_words[language] = set(word_list)
        self._stop_words = self._cached_stop_words[language]

    @staticmethod
    def remove_punctuation(content):
        if not isinstance(content, str):
            content = content.decode('utf-8')
        tbl = dict.fromkeys((ord(x) for x in string.punctuation))
        return content.translate(tbl)

    @staticmethod
    def candidate_words(stripped_input):
        return re.split(SPACE_SYMBOLS, stripped_input)

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        stats = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        i = 0
        for word in candidate_words:
            i += 1
            if word.lower() in self._stop_words:
                overlapping_stopwords.append(word.lower())
        stats.set_word_count(i)
        stats.set_stopword_count(len(overlapping_stopwords))
        stats.set_stop_words(overlapping_stopwords)
        return stats