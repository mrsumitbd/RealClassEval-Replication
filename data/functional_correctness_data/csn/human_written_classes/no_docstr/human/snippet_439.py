from typing import IO, List, Union, cast

class Hider:

    def __init__(self, input_image: Union[str, IO[bytes]], message: str, encoding: str='UTF-8', auto_convert_rgb: bool=False):
        self._index = 0
        message_length = len(message)
        assert message_length != 0, 'message length is zero'
        image = open_image(input_image)
        if image.mode not in ['RGB', 'RGBA']:
            if not auto_convert_rgb:
                print(f'The mode of the image is not RGB. Mode is {image.mode}')
                answer = input('Convert the image to RGB ? [Y / n]\n') or 'Y'
                if answer.lower() == 'n':
                    raise Exception('Not a RGB image.')
            image = image.convert('RGB')
        self.encoded_image = image.copy()
        image.close()
        message = str(message_length) + ':' + str(message)
        self._message_bits = ''.join(a2bits_list(message, encoding))
        self._message_bits += '0' * ((3 - len(self._message_bits) % 3) % 3)
        width, height = self.encoded_image.size
        npixels = width * height
        self._len_message_bits = len(self._message_bits)
        if self._len_message_bits > npixels * 3:
            raise Exception(f'The message you want to hide is too long: {message_length}')

    def encode_another_pixel(self):
        return True if self._index + 3 <= self._len_message_bits else False

    def encode_pixel(self, coordinate: tuple):
        if self.encoded_image.mode == 'RGBA':
            r, g, b, *a = cast(tuple[int, int, int, int], self.encoded_image.getpixel(coordinate))
        else:
            r, g, b, *a = cast(tuple[int, int, int], self.encoded_image.getpixel(coordinate))
        r = setlsb(r, self._message_bits[self._index])
        g = setlsb(g, self._message_bits[self._index + 1])
        b = setlsb(b, self._message_bits[self._index + 2])
        if self.encoded_image.mode == 'RGBA':
            self.encoded_image.putpixel(coordinate, (r, g, b, *a))
        else:
            self.encoded_image.putpixel(coordinate, (r, g, b))
        self._index += 3