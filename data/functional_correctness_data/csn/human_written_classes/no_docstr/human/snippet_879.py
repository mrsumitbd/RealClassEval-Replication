import zipfile
import dataclasses

class UnicodeData:

    def __init__(self, version, cjk_check=True):
        self.changed = []
        table = [None] * 1114112
        for s in UcdFile(UNICODE_DATA, version):
            char = int(s[0], 16)
            table[char] = from_row(s)
        cjk_ranges_found = []
        field = None
        for i in range(0, 1114112):
            s = table[i]
            if s:
                if s.name[-6:] == 'First>':
                    s.name = ''
                    field = dataclasses.astuple(s)[:15]
                elif s.name[-5:] == 'Last>':
                    if s.name.startswith('<CJK Ideograph'):
                        cjk_ranges_found.append((field[0], s.codepoint))
                    s.name = ''
                    field = None
            elif field:
                table[i] = from_row(('%X' % i,) + field[1:])
        if cjk_check and cjk_ranges != cjk_ranges_found:
            raise ValueError('CJK ranges deviate: have %r' % cjk_ranges_found)
        self.filename = UNICODE_DATA % ''
        self.table = table
        self.chars = list(range(1114112))
        if version != '3.2.0':
            self.aliases = []
            pua_index = NAME_ALIASES_START
            for char, name, abbrev in UcdFile(NAME_ALIASES, version):
                char = int(char, 16)
                self.aliases.append((name, char))
                self.table[pua_index].name = name
                pua_index += 1
            assert pua_index - NAME_ALIASES_START == len(self.aliases)
            self.named_sequences = []
            assert pua_index < NAMED_SEQUENCES_START
            pua_index = NAMED_SEQUENCES_START
            for name, chars in UcdFile(NAMED_SEQUENCES, version):
                chars = tuple((int(char, 16) for char in chars.split()))
                assert 2 <= len(chars) <= 4, 'change the Py_UCS2 array size'
                assert all((c <= 65535 for c in chars)), 'use Py_UCS4 in the NamedSequence struct and in unicodedata_lookup'
                self.named_sequences.append((name, chars))
                self.table[pua_index].name = name
                pua_index += 1
            assert pua_index - NAMED_SEQUENCES_START == len(self.named_sequences)
        self.exclusions = {}
        for char, in UcdFile(COMPOSITION_EXCLUSIONS, version):
            char = int(char, 16)
            self.exclusions[char] = 1
        widths = [None] * 1114112
        for char, (width,) in UcdFile(EASTASIAN_WIDTH, version).expanded():
            widths[char] = width
        for i in range(0, 1114112):
            if table[i] is not None:
                table[i].east_asian_width = widths[i]
        self.widths = widths
        for char, (propname, *propinfo) in UcdFile(DERIVED_CORE_PROPERTIES, version).expanded():
            if propinfo:
                continue
            if table[char]:
                table[char].binary_properties.add(propname)
        for char_range, value in UcdFile(LINE_BREAK, version):
            if value not in MANDATORY_LINE_BREAKS:
                continue
            for char in expand_range(char_range):
                table[char].binary_properties.add('Line_Break')
        quickchecks = [0] * 1114112
        qc_order = 'NFD_QC NFKD_QC NFC_QC NFKC_QC'.split()
        for s in UcdFile(DERIVEDNORMALIZATION_PROPS, version):
            if len(s) < 2 or s[1] not in qc_order:
                continue
            quickcheck = 'MN'.index(s[2]) + 1
            quickcheck_shift = qc_order.index(s[1]) * 2
            quickcheck <<= quickcheck_shift
            for char in expand_range(s[0]):
                assert not quickchecks[char] >> quickcheck_shift & 3
                quickchecks[char] |= quickcheck
        for i in range(0, 1114112):
            if table[i] is not None:
                table[i].quick_check = quickchecks[i]
        with open_data(UNIHAN, version) as file:
            zip = zipfile.ZipFile(file)
            if version == '3.2.0':
                data = zip.open('Unihan-3.2.0.txt').read()
            else:
                data = zip.open('Unihan_NumericValues.txt').read()
        for line in data.decode('utf-8').splitlines():
            if not line.startswith('U+'):
                continue
            code, tag, value = line.split(None, 3)[:3]
            if tag not in ('kAccountingNumeric', 'kPrimaryNumeric', 'kOtherNumeric'):
                continue
            value = value.strip().replace(',', '')
            i = int(code[2:], 16)
            if table[i] is not None:
                table[i].numeric_value = value
        sc = self.special_casing = {}
        for data in UcdFile(SPECIAL_CASING, version):
            if data[4]:
                continue
            c = int(data[0], 16)
            lower = [int(char, 16) for char in data[1].split()]
            title = [int(char, 16) for char in data[2].split()]
            upper = [int(char, 16) for char in data[3].split()]
            sc[c] = (lower, title, upper)
        cf = self.case_folding = {}
        if version != '3.2.0':
            for data in UcdFile(CASE_FOLDING, version):
                if data[1] in 'CF':
                    c = int(data[0], 16)
                    cf[c] = [int(char, 16) for char in data[2].split()]

    def uselatin1(self):
        self.chars = list(range(256))