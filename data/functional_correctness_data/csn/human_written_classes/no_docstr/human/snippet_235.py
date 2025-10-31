from pygments.formatters.html import escape_html

class Column:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = ''
        self.type = ''
        self.data = []
        self.classes = []
        self.classstr = ''

    def detect_right_aligned(self):
        ra = self.type in {'bool8', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'date32', 'time64'}
        if ra:
            self.classes.append('r')

    def process_data(self):
        dot_width = 0
        if self.type in ['time64']:
            for value in self.data:
                if '.' in value:
                    t = len(value) - value.rindex('.')
                    dot_width = max(dot_width, t)
        for i, value in enumerate(self.data):
            value = escape_html(value)
            if value == 'NA':
                value = '<span class=NA>NA</span>'
            if value == '…':
                value = '<span class=dim>…</span>'
            if dot_width:
                if '.' in value:
                    t = len(value) - value.rindex('.')
                else:
                    t = 0
                value += ' ' * (dot_width - t)
            if self.type == 'time64':
                value = value.replace('T', '<span class=dim>T</span>')
            self.data[i] = value