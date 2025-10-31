class StringTool:
    """ Common string function
    """

    @staticmethod
    def strip(a_str):
        return a_str.strip() if a_str else ''

    @staticmethod
    def to_str(a_str):
        return str(a_str) if a_str else ''

    @staticmethod
    def detokenize(tokens):
        sentence_text = ' '.join(tokens)
        sentence_text = sentence_text.replace(' , , ', ', ')
        sentence_text = sentence_text.replace(' , ', ', ').replace('“ ', '“').replace(' ”', '”')
        sentence_text = sentence_text.replace(' ! ', '! ').replace(" 'll ", "'ll ").replace(" 've ", "'ve ").replace(" 're ", "'re ").replace(" 'd ", "'d ")
        sentence_text = sentence_text.replace(" 's ", "'s ")
        sentence_text = sentence_text.replace(" 'm ", "'m ")
        sentence_text = sentence_text.replace(" ' ", "' ")
        sentence_text = sentence_text.replace(' ; ', '; ')
        sentence_text = sentence_text.replace(' : ', ': ')
        sentence_text = sentence_text.replace('( ', '(')
        sentence_text = sentence_text.replace(' )', ')')
        sentence_text = sentence_text.replace(' ?', '?')
        sentence_text = sentence_text.replace(" n't ", "n't ")
        sentence_text = sentence_text.replace('  ', ' ')
        sentence_text = sentence_text.replace('``', '“').replace("''", '”')
        sentence_text = sentence_text.replace('“ ', '“').replace(' ”', '”')
        if sentence_text[-2:] in (' .', ' :', ' ?', ' !', ' ;'):
            sentence_text = sentence_text[:-2] + sentence_text[-1]
        sentence_text = sentence_text.strip()
        return sentence_text