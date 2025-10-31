import bitstring

class Register:

    def __init__(self, description, address, length, bitfields):
        """Class initializer

        Parameter:
        'description' : (str)       Description
        'address'     : (bitstring) Address. Shall be 'None' is address is not applicable
        'length'      : (int)       Length in bits
        'bitfields'   : (dict)      A dictionary of 'hwio.register.Bitfield' objects

        Return:
        An instance of class

        """
        self.description = description
        self.address = address
        self.length = length
        if bitfields is not None:
            bits = []
            for bitfield in sorted(bitfields.values(), key=lambda bitfield: bitfield.bit_high, reverse=True):
                bits += list(range(bitfield.bit_high, bitfield.bit_low - 1, -1))
            if bits != list(range(self.length - 1, -1, -1)):
                logger.critical(f"Bitfields gap or overlap in '{self.description}' register")
                raise RegisterCritical
        self.bitfields = bitfields

    @property
    def value(self):
        """Get register value

        Parameter:
        None

        Return:
        (bitstring) Combined register bitfields

        """
        value = bitstring.BitArray(self.length)
        if self.length != 0:
            for bitfield in self.bitfields.values():
                value[self.length - bitfield.bit_high - 1:self.length - bitfield.bit_low] = bitstring.BitArray(f'{bitfield.fmt}:{bitfield.bit_high - bitfield.bit_low + 1}={(bitfield.values[bitfield.value] if bitfield.values is not None else bitfield.value)}')
        return value

    @value.setter
    def value(self, value):
        """Set register value

        Parameter:
        'value' : (bitstring) Combined register bitfields

        Return:
        None

        """
        if value.length != self.length:
            logger.critical(f"Size mismatch between value and '{self.description}' register")
            raise RegisterCritical
        if self.length != 0:
            for bitfield in self.bitfields.values():
                bitfield.value = value[self.length - bitfield.bit_high - 1:self.length - bitfield.bit_low].unpack(f'{bitfield.fmt}:{bitfield.bit_high - bitfield.bit_low + 1}')[0]
                if bitfield.values is not None:
                    bitfield.value = next((item[0] for item in bitfield.values.items() if item[1] == bitfield.value), None)
        return None

    def log(self):
        """Log register bitfields data in human-readable form

        Parameter:
        None

        Return:
        None

        """
        if self.address is not None:
            logger.debug(f"Register '{self.description}', address: 0x{self.address.hex.upper()}, length: {self.length} bits, value: 0b{self.value.bin}")
        else:
            logger.debug(f"Register '{self.description}', length: {self.length} bits, value: 0b{self.value.bin}")
        if self.bitfields is not None:
            bitfields = sorted(self.bitfields.values(), key=lambda bitfield: bitfield.bit_high, reverse=True)
            bits_width = 0
            value_bin_width = 0
            value_hex_width = 0
            value_int_width = 0
            value_str_width = 0
            for bitfield in bitfields:
                bit_value = bitstring.Bits(f'{bitfield.fmt}:{bitfield.bit_high - bitfield.bit_low + 1}={(bitfield.values[bitfield.value] if bitfield.values is not None else bitfield.value)}')
                if bits_width < len(bitfield.bits):
                    bits_width = len(bitfield.bits)
                if value_bin_width < len(bit_value.bin):
                    value_bin_width = len(bit_value.bin)
                if value_hex_width < len((bitstring.Bits(4 - len(bit_value) % 4) + bit_value).hex if len(bit_value) % 4 != 0 else bit_value.hex):
                    value_hex_width = len((bitstring.Bits(4 - len(bit_value) % 4) + bit_value).hex if len(bit_value) % 4 != 0 else bit_value.hex)
                if bitfield.fmt == 'uint':
                    if value_int_width < len(str(bit_value.uint)):
                        value_int_width = len(str(bit_value.uint))
                elif bitfield.fmt == 'int':
                    if value_int_width < len(str(bit_value.int)):
                        value_int_width = len(str(bit_value.int))
                if bitfield.values is not None:
                    if value_str_width < len(str(bitfield.value)):
                        value_str_width = len(str(bitfield.value))
            for bitfield in bitfields:
                bit_value = bitstring.Bits(f'{bitfield.fmt}:{bitfield.bit_high - bitfield.bit_low + 1}={(bitfield.values[bitfield.value] if bitfield.values is not None else bitfield.value)}')
                bits = f'{bitfield.bits:{bits_width}}'
                value_bin = f'0b{bit_value.bin:{value_bin_width}}'
                value_hex = f'0x{((bitstring.Bits(4 - len(bit_value) % 4) + bit_value).hex.upper() if len(bit_value) % 4 != 0 else bit_value.hex.upper()):{value_hex_width}}'
                if bitfield.fmt == 'uint':
                    value_int = f'{bit_value.uint:{value_int_width}}'
                elif bitfield.fmt == 'int':
                    value_int = f'{bit_value.int:{value_int_width}}'
                if bitfield.values is not None:
                    value_str = f' {bitfield.value:{value_str_width}}'
                else:
                    value_str = ' ' * (value_str_width + 1)
                if value_str == ' ':
                    value_str = ''
                logger.debug(f'{bits} = {value_bin} {value_hex} {value_int}{value_str} {bitfield.description}')
        return None