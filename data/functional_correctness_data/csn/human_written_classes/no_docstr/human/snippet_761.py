import re

class LabelFormatOpts:

    def __init__(self, fmt_str, base=10, digits=2):
        base_char = p2b_dict[base]
        data = _fmt_re.findall(fmt_str)
        ft = [item[0] for item in data if item[0] != '']
        if ft:
            if all((el == ft[0] for el in ft)):
                base_char = ft[0][-1]
                base, digits = (b2p_dict.get(base_char), int(ft[0][2:-1]))
            else:
                raise ValueError(f'{fmt_str} Define different formatter for no variable.')
        new_field_fmt = '{{no:0{0}{1}}}'.format(digits, base_char)
        self.origin_fmt = fmt_str
        self.normalized_fmt = _fmt_re.sub(new_field_fmt, fmt_str)
        fr_dict = {'b': '(?P<no>[01]{{{0}}})'.format(digits), 'o': '(?P<no>[0-7]{{{0}}})'.format(digits), 'd': '(?P<no>[0-9]{{{0}}})'.format(digits), 'x': '(?P<no>[0-9a-f]{{{0}}})'.format(digits), 'X': '(?P<no>[0-9A-Z]{{{0}}})'.format(digits)}
        self.parse_re = re.compile(self.normalized_fmt.replace(new_field_fmt, fr_dict[base_char]))
        self.base = base
        self.digits = digits
        self.base_char = base_char

    def value2label(self, value: int) -> str:
        return self.normalized_fmt.format(no=value)

    def label2value(self, label: str) -> int:
        m = self.parse_re.match(label)
        if m:
            return int(m.group('no'), base=self.base)
        raise ValueError(f'Error Value {label}')