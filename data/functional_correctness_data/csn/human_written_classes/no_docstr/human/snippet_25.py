from typing import ClassVar

class Stemmer:
    STOP_WORDS: ClassVar[set[str]] = set("a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves".split())
    PREFIXES = set('auto be fore over re un under'.split())
    SUFFIXES = set('able al ance ant ate ed en er ful hood ing ion ish ity ive ize less ly ment ness ous ship sion tion y'.split())
    VOWELS = set('aeiou')
    PLURALIZATION = set('s es ies'.split())

    def stem(self, word: str) -> str:
        if word in self.STOP_WORDS:
            return word
        if word in self.PREFIXES:
            return word
        for suffix in self.SUFFIXES | self.PLURALIZATION:
            if word.endswith(suffix):
                return self._stem(word[:-len(suffix)])
        return word

    def _stem(self, word: str) -> str:
        if word.endswith('e'):
            return word[:-1]
        if word.endswith('y') and word[-2] not in self.VOWELS:
            return word[:-1]
        return word

    def __call__(self, word: str) -> str:
        return self.stem(word)