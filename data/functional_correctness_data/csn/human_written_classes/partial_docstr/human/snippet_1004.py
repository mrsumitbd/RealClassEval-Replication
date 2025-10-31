from dragonpy.Dragon32.dragon_charmap import COLORS, INVERTED, NORMAL, get_hex_color
import tkinter

class TkImageFont:
    """
    Important is that image must be bind to a object, without:
    the garbage-collection by Python will "remove" the created images in Tkinter.Canvas!
    """

    def __init__(self, chars_dict, scale_factor):
        assert isinstance(scale_factor, int)
        assert scale_factor > 0
        self.chars_dict = chars_dict
        self.scale_factor = scale_factor
        temp = chars_dict['X']
        self.width_real = len(temp[0])
        self.height_real = len(temp)
        self.width_scaled = self.width_real * self.scale_factor
        self.height_scaled = self.height_real * self.scale_factor
        log.critical('Every character is %ipx x %ipx (incl. scale factor: %i)', self.width_scaled, self.height_scaled, self.scale_factor)

    def get_char(self, char, color):
        log.critical('Generate char %s %s', repr(char), color)
        try:
            char_data = self.chars_dict[char]
        except KeyError:
            log.log(99, 'Error: character %s is not in CHARS_DICT !', repr(char))
            return self.get_char(char='?', color=color)
        foreground, background = get_hex_color(color)
        foreground = f'#{foreground}'
        background = f'#{background}'
        img = tkinter.PhotoImage(width=self.width_scaled, height=self.height_scaled)
        for y, line in enumerate(char_data):
            for x, bit in enumerate(line):
                if bit == BACKGROUND_CHAR:
                    color = background
                else:
                    assert bit == FOREGROUND_CHAR
                    color = foreground
                img.put(color, (x, y))
        if self.scale_factor > 1:
            img = img.zoom(self.scale_factor, self.scale_factor)
        return img