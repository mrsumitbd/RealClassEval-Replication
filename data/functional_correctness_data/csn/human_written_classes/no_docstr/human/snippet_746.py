import re

class Toolkit:

    @staticmethod
    def create_table_array(t, put_extractions=False):
        rows = t['rows']
        tt = []
        max_cols = t['features']['max_cols_in_a_row']
        for r in rows:
            new_r = ['' for xx in range(max_cols)]
            for i, c in enumerate(r['cells']):
                text = c['text']
                text = text.lower()
                text = text.strip()
                if put_extractions and 'data_extraction' in c:
                    data_extractions = c['data_extraction']
                    for key in data_extractions.keys():
                        text += ' DUMMY' + key.upper()
                new_r[i] = text.strip()
            tt.append(new_r)
        return tt

    @staticmethod
    def regulize_cells(t):
        for r in t:
            for i in range(len(r)):
                r[i] = re.sub('[0-9]', 'NUM', r[i])
                for x in re.findall('([a-z][a-z][a-z]+@)', r[i]):
                    r[i] = re.sub(x, 'EMAILNAME ', r[i])

    @staticmethod
    def clean_cells(t):
        for r in t:
            for i in range(len(r)):
                r[i] = re.sub('[^\\x00-\\x7F]', ' ', r[i])
                r[i] = re.sub('[^\\s\\w\\.\\-\\$_%\\^&*#~+@"\']', ' ', r[i])
                for x in re.findall('(\\.[a-z])', r[i]):
                    r[i] = re.sub('\\.{0}'.format(x[1]), ' {0}'.format(x[1]), r[i])
                r[i] = re.sub('\\s+', ' ', r[i])
                r[i] = r[i].strip()