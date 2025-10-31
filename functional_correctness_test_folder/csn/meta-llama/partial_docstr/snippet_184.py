
class Encoder:

    def needsEncoding(self, s):
        '''
        Get whether string I{s} contains special characters.
        @param s: A string to check.
        @type s: str
        @return: True if needs encoding.
        @rtype: boolean
        '''
        special_chars = set('"\'<>\\&')
        return any(c in special_chars for c in s)

    def encode(self, s):
        '''
        Encode a string to replace special characters with their corresponding HTML entities.
        @param s: A string to encode.
        @type s: str
        @return: The encoded string.
        @rtype: str
        '''
        encoding_map = {
            '"': '&quot;',
            '\'': '&#39;',
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '\\': '&#92;'
        }
        return ''.join(encoding_map.get(c, c) for c in s)

    def decode(self, s):
        '''
        Decode a string to replace HTML entities with their corresponding special characters.
        @param s: A string to decode.
        @type s: str
        @return: The decoded string.
        @rtype: str
        '''
        decoding_map = {
            '&quot;': '"',
            '&#39;': '\'',
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&#92;': '\\'
        }
        for entity, char in decoding_map.items():
            s = s.replace(entity, char)
        return s
