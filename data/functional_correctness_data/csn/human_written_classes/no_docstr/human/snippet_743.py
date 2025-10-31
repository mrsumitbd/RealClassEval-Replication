class CP437:
    table = '\x00☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼ !"' + "#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]" + '^_`abcdefghijklmnopqrstuvwxyz{|}~⌂ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■\xa0'

    @staticmethod
    def ord(c):
        return CP437.table.find(c)

    @staticmethod
    def chr(o):
        if not 0 <= o < 256:
            raise ValueError
        return CP437.table[o]

    @staticmethod
    def from_Unicode(s):
        res = []
        for c in s:
            if c in CP437.table:
                res.append(CP437.ord(c))
            else:
                res.extend(c.encode('utf-8'))
        return res