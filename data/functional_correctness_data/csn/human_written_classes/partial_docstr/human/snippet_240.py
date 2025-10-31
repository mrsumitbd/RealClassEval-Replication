from underthesea.utils.vietnamese_ipa_rules import codas, nuclei, onsets, onoffglides, onglides, offglides
import regex

class Syllable:
    """
    Syllable class
    """

    def __init__(self, text):
        self.text = text
        non_tone_letters, tone = VIETNAMESE.analyze_tone(text)
        self.tone = tone
        a = '[aăâ]'
        o = '[oôơ]'
        u = '[uư]'
        double = f'oo|i{a}|iê|yê|y{a}|{u}{o}|{u}{a}|ay|ây|ua'
        v = '(?P<V>[aăâeêuưyoôơi]|' + double + ')'
        vec = '(?P<V>ê)'
        wu = '(?P<w>[u])'
        vye = '(?P<V>yê)'
        vya = f'(?P<V>y{a})'
        consonants = 'gi|qu|ch|gh|kh|ng|ngh|nh|ph|th|tr|[bcdđghklmnpqrstvx]'
        conda = consonants + '|[uio]'
        c1 = '(?P<C1>' + consonants + ')?'
        c2 = '(?P<C2>' + conda + ')?'
        patterns = ['^' + c1 + '(?P<w>[u])(?P<V>[yâ])' + c2 + '$', '^' + c1 + '(?P<w>[o])(?P<V>[eaă])' + c2 + '$', '^' + c1 + v + c2 + '$', '^' + c1 + wu + vec + c2 + '$', '^' + c1 + wu + vye + c2 + '$', '^' + c1 + wu + vya + c2 + '$']
        pattern = '(' + '|'.join(patterns) + ')'
        matched = regex.match(pattern, non_tone_letters)
        self.matched = matched
        if not matched:
            raise Exception(f'Text {text} not matched')

    def _util_reverse_dict(self, d):
        result = {}
        for k in d:
            for v in d[k]:
                result[v] = k
        return result

    def generate_ipa(self, dialect: str='north', eight: bool=False, tone: str='number'):
        """Generate ipa of the syllable

        Vietnamese syllabic structure (Trang 2022)
        syllable = onset + rhyme + tone
        rhyme = medial + nuclear vowel + (coda)

        Args:
            dialect (str): Either the `string` `"north"` or `"south"`. Default: `north`
            eight (boolean): If true, use eight tone format, else use six tone format. Default: `False`
            tone (str): Either the `string` `"ipa"` or `"number"`. Default: `number`

        Returns:
            A `string`. Represents ipa of the syllable
        """
        groups = self.matched.groupdict()
        map_w = {'o': 'ʷ', 'u': 'ʷ'}
        c1, w, v, c2 = (groups['C1'], groups['w'], groups['V'], groups['C2'])
        ipa_w = ''
        if w:
            ipa_w = map_w[w]
        nuclei.update(onglides)
        nuclei.update(offglides)
        nuclei.update(onoffglides)
        ipa_v = nuclei[v]
        if c1:
            ipa_c1 = onsets[c1]
        else:
            ipa_c1 = ''
            if v == 'a':
                ipa_v = 'aː'
        if ipa_c1 == '':
            ipa_c1 = ''
        if c2:
            ipa_c2 = codas[c2]
            if c2 in ['o', 'i', 'u', 'y']:
                if v == 'a':
                    if c2 == 'o':
                        ipa_v = 'aː'
                    elif c2 in ['u', 'ă', 'y']:
                        ipa_v = 'a'
                if v == 'o' and c2 == 'o':
                    ipa_v = 'ↄ:'
                    ipa_c2 = ''
                if v == 'y' and c2 == 'u':
                    ipa_v = 'i'
                if v == 'u' and c2 == 'y':
                    ipa_c2 = 'i'
        else:
            ipa_c2 = ''
        map_tone_ipa = {VIETNAMESE.TONE.HIGH_LEVEL: '˧˧', VIETNAMESE.TONE.MID_FALLING: '˨˩', VIETNAMESE.TONE.LOW_FALLING_RISING: '˨˩', VIETNAMESE.TONE.HIGH_FALLING_RISING_GLOTTALIZED: '˧˥'}
        map_tone_number = {VIETNAMESE.TONE.HIGH_LEVEL: '³³', VIETNAMESE.TONE.MID_FALLING: '³²', VIETNAMESE.TONE.RISING: '²⁴', VIETNAMESE.TONE.LOW_FALLING_RISING: '³¹²', VIETNAMESE.TONE.HIGH_FALLING_RISING_GLOTTALIZED: '³ˀ⁵', VIETNAMESE.TONE.LOW_GLOTTALIZED: '²¹ˀ'}
        if tone == 'number':
            map_t = map_tone_number
        else:
            map_t = map_tone_ipa
        ipa_t = map_t[self.tone]
        ons = ipa_c1
        cod = ipa_c2
        nuc = ipa_v
        ton = ipa_t
        if ons == 'z' and nuc == 'e':
            nuc = 'iə'
        if ons == 'ɣ' and nuc == 'i':
            ons = 'z'
        if ons == '':
            ons = 'ʔ'
        if ons == 'ʂ':
            ons = 's'
        if dialect == 'north':
            if ons in ['j', 'r']:
                ons = 'z'
            elif ons in ['c', 'ʈ']:
                ons = 'tɕ'
            elif ons == 'ʂ':
                ons = 's'
        if dialect == 'south':
            if cod in ['ŋ', 'k'] and nuc in ['u', 'o', 'ↄ']:
                if cod == 'ŋ':
                    cod = 'ŋ͡m'
                elif cod == 'k':
                    cod = 'k͡p'
        if cod in ['ŋ', 'k']:
            if nuc == 'ɛ':
                nuc = 'ɛː'
            if nuc == 'e':
                nuc = 'eː'
        if nuc == 'aː':
            if cod == 'c':
                nuc = 'ɛ'
            if cod == 'ɲ':
                nuc = 'ɛ'
        if cod in ['c', 'ɲ']:
            if cod == 'c':
                cod = 'k'
            if cod == 'ɲ':
                cod = 'ŋ'
        if not cod and nuc in ['aː', 'əː']:
            if nuc == 'aː':
                nuc = 'a'
            if nuc == 'əː':
                nuc = 'ə'
        if eight:
            if cod in ['p', 't', 'k']:
                if self.tone == VIETNAMESE.TONE.RISING:
                    ton = '⁴⁵'
                elif self.tone == VIETNAMESE.TONE.LOW_GLOTTALIZED:
                    ton = '²¹'
        ipa = ons + ipa_w + nuc + cod + ton
        return ipa