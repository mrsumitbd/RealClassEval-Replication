from typing import IO, List, Union, cast

class Revealer:

    def __init__(self, encoded_image: Union[str, IO[bytes]], encoding: str='UTF-8', close_file: bool=True):
        self.encoded_image = open_image(encoded_image)
        self._encoding_length = ENCODINGS[encoding]
        self._buff, self._count = (0, 0)
        self._bitab: List[str] = []
        self._limit: Union[None, int] = None
        self.secret_message = ''
        self.close_file = close_file

    def decode_pixel(self, coordinate: tuple):
        pixel = cast(tuple[int, int, int] | tuple[int, int, int, int], self.encoded_image.getpixel(coordinate))
        if self.encoded_image.mode == 'RGBA':
            pixel = pixel[:3]
        for color in pixel:
            self._buff += (color & 1) << self._encoding_length - 1 - self._count
            self._count += 1
            if self._count == self._encoding_length:
                self._bitab.append(chr(self._buff))
                self._buff, self._count = (0, 0)
                if self._bitab[-1] == ':' and self._limit is None:
                    if ''.join(self._bitab[:-1]).isdigit():
                        self._limit = int(''.join(self._bitab[:-1]))
                    else:
                        raise IndexError('Impossible to detect message.')
        if len(self._bitab) - len(str(self._limit)) - 1 == self._limit:
            self.secret_message = ''.join(self._bitab)[len(str(self._limit)) + 1:]
            if self.close_file:
                self.encoded_image.close()
            return True
        else:
            return False