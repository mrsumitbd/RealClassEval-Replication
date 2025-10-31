from dragonpy.Dragon32.dragon_font import CHARS_DICT, TkImageFont
from dragonpy.Dragon32.dragon_charmap import get_charmap_dict
from dragonpy.Dragon32 import dragon_charmap
import tkinter

class MC6847_TextModeCanvas:
    """
    MC6847 Video Display Generator (VDG) in Alphanumeric Mode.
    This display mode consumes 512 bytes of memory and is a 32 character wide screen with 16 lines.

    Here we only get the "write into Display RAM" information from the CPU-Thread
    from display_queue.

    The Display Tkinter.Canvas() which will be filled with Tkinter.PhotoImage() instances.
    Every displayed character is a Tkinter.PhotoImage()
    """

    def __init__(self, root):
        self.rows = 32
        self.columns = 16
        scale_factor = 2
        self.tk_font = TkImageFont(CHARS_DICT, scale_factor)
        self.total_width = self.tk_font.width_scaled * self.rows
        self.total_height = self.tk_font.height_scaled * self.columns
        foreground, background = dragon_charmap.get_hex_color(dragon_charmap.NORMAL)
        self.canvas = tkinter.Canvas(root, width=self.total_width, height=self.total_height, bd=0, highlightthickness=0, bg=f'#{background}')
        self.charmap = get_charmap_dict()
        self.image_cache = {}
        self.images_map = {}
        self.init_img = self.tk_font.get_char(char='?', color=dragon_charmap.INVERTED)
        for row in range(self.rows + 1):
            for column in range(self.columns + 1):
                x = self.tk_font.width_scaled * row
                y = self.tk_font.height_scaled * column
                image_id = self.canvas.create_image(x, y, image=self.init_img, state='normal', anchor=tkinter.NW)
                self.images_map[x, y] = image_id

    def write_byte(self, cpu_cycles, op_address, address, value):
        try:
            image = self.image_cache[value]
        except KeyError:
            char, color = self.charmap[value]
            image = self.tk_font.get_char(char, color)
            self.image_cache[value] = image
        position = address - 1024
        column, row = divmod(position, self.rows)
        x = self.tk_font.width_scaled * row
        y = self.tk_font.height_scaled * column
        image_id = self.images_map[x, y]
        self.canvas.itemconfigure(image_id, image=image)