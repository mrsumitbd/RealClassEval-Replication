
class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
    '''

    def __init__(self, data):
        self.code_pages = data

    @staticmethod
    def get_encoding_name(encoding):
        encoding_map = {
            'cp437': 'cp437',
            'cp850': 'cp850',
            'cp860': 'cp860',
            'cp863': 'cp863',
            'cp865': 'cp865',
            'cp866': 'cp866',
            'cp852': 'cp852',
            'cp858': 'cp858',
            'cp857': 'cp857',
            'cp737': 'cp737',
            'iso8859_7': 'iso-8859-7',
            'cp1252': 'windows-1252',
            'cp1253': 'windows-1253',
            'cp1254': 'windows-1254',
            'cp1255': 'windows-1255',
            'cp1256': 'windows-1256',
            'cp1257': 'windows-1257',
            'cp1258': 'windows-1258',
            'cp932': 'cp932',
            'cp936': 'gbk',
            'cp949': 'cp949',
            'cp950': 'cp950',
            'cp1251': 'windows-1251',
            'cp866': 'cp866',
            'cp855': 'cp855',
            'cp864': 'cp864',
            'iso8859_2': 'iso-8859-2',
            'iso8859_15': 'iso-8859-15',
            'tis_620': 'tis-620',
            'katakana': 'x-cp20261'
        }
        return encoding_map.get(encoding.lower(), 'cp437')

    def get_code_page_data(self, encoding):
        '''Return the encoding data.'''
        encoding_name = self.get_encoding_name(encoding)
        return self.code_pages.get(encoding_name)
