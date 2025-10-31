class IgnoreWordsFilterFactory:

    def __init__(self, words):
        self.words = words

    def __call__(self, tokenizer):
        return IgnoreWordsFilter(tokenizer, self.words)