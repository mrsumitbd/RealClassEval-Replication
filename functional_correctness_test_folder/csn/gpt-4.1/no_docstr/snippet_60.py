
class CodePageManager:

    _encoding_map = {
        65001: 'utf-8',
        1200: 'utf-16le',
        1201: 'utf-16be',
        20127: 'ascii',
        28591: 'iso-8859-1',
        28592: 'iso-8859-2',
        28593: 'iso-8859-3',
        28594: 'iso-8859-4',
        28595: 'iso-8859-5',
        28596: 'iso-8859-6',
        28597: 'iso-8859-7',
        28598: 'iso-8859-8',
        28599: 'iso-8859-9',
        28605: 'iso-8859-15',
        936: 'gb2312',
        950: 'big5',
        932: 'shift_jis',
        949: 'ks_c_5601-1987',
        1250: 'windows-1250',
        1251: 'windows-1251',
        1252: 'windows-1252',
        1253: 'windows-1253',
        1254: 'windows-1254',
        1255: 'windows-1255',
        1256: 'windows-1256',
        1257: 'windows-1257',
        1258: 'windows-1258',
    }

    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        if isinstance(encoding, int):
            return CodePageManager._encoding_map.get(encoding, None)
        elif isinstance(encoding, str):
            return encoding.lower()
        else:
            return None

    def get_encoding_name(self, encoding):
        return CodePageManager.get_encoding_name(encoding)
