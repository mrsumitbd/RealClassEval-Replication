import bitstring
import hwio.register
import hwio.i2c

class FTDIEEPROM:

    def __init__(self, owner, description, eeprom_type, manufacturer, product, serial_number, drive, slew, hysteresis):
        """Class initializer

        Parameter:
        'owner'         : (object)      Instance of the FTDI class for the device this EEPROM is connected to
        'description'   : (str)         Device description
        'eeprom_type'   : (str)         EEPROM type: 'x56', 'x66'
        'manufacturer'  : (str or None) USB iManufacturer
        'product'       : (str or None) USB iProduct
        'serial_number' : (str or None) USB iSerialNumber
        'drive'         : (str)         Output drive current: '4 mA', '8 mA', '12 mA', '16 mA'
        'slew'          : (str)         Output slew rate: 'fast', 'slow'
        'hysteresis'    : (str)         Input hysteresis: 'no', 'yes'

        Return:
        An instance of class

        """
        self.owner = owner
        self.description = description
        if PRODUCT_IDS[self.owner.device.idProduct] not in ['FT232H', 'FT2232H', 'FT4232H']:
            logger.critical(f'FAIL: Wrong USB idProduct: 0x{self.owner.device.idProduct:04X}')
            raise FTDICritical
        if eeprom_type == 'x56':
            self.eeprom_size = 128
        elif eeprom_type == 'x66':
            self.eeprom_size = 256
        else:
            logger.critical(f'FAIL: Wrong EEPROM type: {eeprom_type}')
            raise FTDICritical
        self.registers = {}
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            offset = 80 * 2
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT2232H', 'FT4232H']:
            offset = 13 * 2
        if manufacturer is not None:
            mfg_str_addr = offset
            mfg_str_value = manufacturer.encode('utf-16be')
            mfg_str_len = 1 + 1 + len(mfg_str_value)
            mfg_str_value = b'\x03' + bytes([mfg_str_len]) + mfg_str_value
            self.registers['usb_mfg_desc'] = hwio.register.Register(description='USB manufacturer string descriptor (iManufacturer)', address=bitstring.Bits(uint=mfg_str_addr // 2, length=8), length=mfg_str_len * 8, bitfields={'mfg_str': hwio.register.Bitfield(bits=f'[{mfg_str_len * 8 - 1}:0]', description='Manufacturer string descriptor (iManufacturer)', fmt='uint', value=bitstring.Bits(bytes=mfg_str_value).uint)})
        else:
            mfg_str_addr = 0
            mfg_str_len = 0
        if product is not None:
            prod_str_addr = offset + mfg_str_len
            prod_str_value = product.encode('utf-16be')
            prod_str_len = 1 + 1 + len(prod_str_value)
            prod_str_value = b'\x03' + bytes([prod_str_len]) + prod_str_value
            self.registers['usb_prod_desc'] = hwio.register.Register(description='USB product string descriptor (iProduct)', address=bitstring.Bits(uint=prod_str_addr // 2, length=8), length=prod_str_len * 8, bitfields={'prod_str': hwio.register.Bitfield(bits=f'[{prod_str_len * 8 - 1}:0]', description='Product string descriptor (iProduct)', fmt='uint', value=bitstring.Bits(bytes=prod_str_value).uint)})
        else:
            prod_str_addr = 0
            prod_str_len = 0
        if serial_number is not None:
            ser_no_str_addr = offset + mfg_str_len + prod_str_len
            ser_no_str_value = serial_number.encode('utf-16be')
            ser_no_str_len = 1 + 1 + len(ser_no_str_value)
            ser_no_str_value = b'\x03' + bytes([ser_no_str_len]) + ser_no_str_value
            self.registers['usb_ser_no_desc'] = hwio.register.Register(description='USB serial number string descriptor (iSerialNumber)', address=bitstring.Bits(uint=ser_no_str_addr // 2, length=8), length=ser_no_str_len * 8, bitfields={'ser_no_str': hwio.register.Bitfield(bits=f'[{ser_no_str_len * 8 - 1}:0]', description='Serial number string descriptor (iSerialNumber)', fmt='uint', value=bitstring.Bits(bytes=ser_no_str_value).uint)})
        else:
            ser_no_str_addr = 0
            ser_no_str_len = 0
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            self.registers['port_cfg'] = hwio.register.Register(description='Port configuration', address=bitstring.Bits('0x00'), length=16, bitfields={'suspend_ac7': hwio.register.Bitfield(bits='[15]', description='Suspend when AC7 pin is low', fmt='uint', values={'no': 0, 'yes': 1}, value='no'), 'reserved_1': hwio.register.Bitfield(bits='[14:11]', description='reserved', fmt='uint', value=0), 'ft1248_flow_control': hwio.register.Bitfield(bits='[10]', description='FT1248 flow control', fmt='uint', values={'yes': 0, 'no': 1}, value='yes'), 'ft1248_bit_order': hwio.register.Bitfield(bits='[9]', description='FT1248 bit order', fmt='uint', values={'msb': 0, 'lsb': 1}, value='msb'), 'ft1248_clock_polarity': hwio.register.Bitfield(bits='[8]', description='FT1248 clock polarity', fmt='uint', values={'low': 0, 'high': 1}, value='low'), 'reserved_0': hwio.register.Bitfield(bits='[7:5]', description='reserved', fmt='uint', value=0), 'port_driver': hwio.register.Bitfield(bits='[4]', description='Port driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_type': hwio.register.Bitfield(bits='[3:0]', description='Port type', fmt='uint', values={'uart': 0, 'fifo_245': 1, 'fifo_cpu': 2, 'fast_serial': 4, 'ft1248': 8}, value='uart')})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT2232H']:
            self.registers['port_cfg'] = hwio.register.Register(description='Port configuration', address=bitstring.Bits('0x00'), length=16, bitfields={'suspend_bc7': hwio.register.Bitfield(bits='[15]', description='Suspend when BC7 pin is low', fmt='uint', values={'no': 0, 'yes': 1}, value='no'), 'reserved_1': hwio.register.Bitfield(bits='[14:12]', description='reserved', fmt='uint', value=0), 'port_b_driver': hwio.register.Bitfield(bits='[11]', description='Port B driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_b_type': hwio.register.Bitfield(bits='[10:8]', description='Port B type', fmt='uint', values={'uart': 0, 'fifo_245': 1, 'fifo_cpu': 2, 'fast_serial': 4}, value='uart'), 'reserved_0': hwio.register.Bitfield(bits='[7:4]', description='reserved', fmt='uint', value=0), 'port_a_driver': hwio.register.Bitfield(bits='[3]', description='Port A driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_a_type': hwio.register.Bitfield(bits='[2:0]', description='Port A type', fmt='uint', values={'uart': 0, 'fifo_245': 1, 'fifo_cpu': 2, 'fast_serial': 4}, value='uart')})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT4232H']:
            self.registers['port_cfg'] = hwio.register.Register(description='Port configuration', address=bitstring.Bits('0x00'), length=16, bitfields={'port_d_driver': hwio.register.Bitfield(bits='[15]', description='Port D driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_d_type': hwio.register.Bitfield(bits='[14:12]', description='Port D type', fmt='uint', values={'uart': 0}, value='uart'), 'port_b_driver': hwio.register.Bitfield(bits='[11]', description='Port B driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_b_type': hwio.register.Bitfield(bits='[10:8]', description='Port B type', fmt='uint', values={'uart': 0}, value='uart'), 'port_c_driver': hwio.register.Bitfield(bits='[7]', description='Port C driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_c_type': hwio.register.Bitfield(bits='[6:4]', description='Port C type', fmt='uint', values={'uart': 0}, value='uart'), 'port_a_driver': hwio.register.Bitfield(bits='[3]', description='Port A driver', fmt='uint', values={'d2xx': 0, 'vcp': 1}, value='vcp'), 'port_a_type': hwio.register.Bitfield(bits='[2:0]', description='Port A type', fmt='uint', values={'uart': 0}, value='uart')})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H', 'FT2232H', 'FT4232H']:
            self.registers['usb_vid'] = hwio.register.Register(description='USB vendor ID (idVendor)', address=bitstring.Bits('0x01'), length=16, bitfields={'usb_vid': hwio.register.Bitfield(bits='[15:0]', description='USB vendor ID (idVendor)', fmt='uint', values={'FTDI': 1027}, value='FTDI')})
            self.registers['usb_pid'] = hwio.register.Register(description='USB product ID (idProduct)', address=bitstring.Bits('0x02'), length=16, bitfields={'usb_pid': hwio.register.Bitfield(bits='[15:0]', description='USB product ID (idProduct)', fmt='uint', values={'FT232H': 24596, 'FT2232H': 24592, 'FT4232H': 24593}, value=PRODUCT_IDS[self.owner.device.idProduct])})
            self.registers['usb_dev_rel_no'] = hwio.register.Register(description='USB device release number (bcdDevice)', address=bitstring.Bits('0x03'), length=16, bitfields={'usb_dev_rel_no': hwio.register.Bitfield(bits='[15:0]', description='USB device release number (bcdDevice)', fmt='uint', values={'FT232H': 2304, 'FT2232H': 1792, 'FT4232H': 2048}, value=PRODUCT_IDS[self.owner.device.idProduct])})
            self.registers['usb_cfg_desc'] = hwio.register.Register(description='USB configuration descriptor (bmAttributes, bMaxPower)', address=bitstring.Bits('0x04'), length=16, bitfields={'max_power': hwio.register.Bitfield(bits='[15:8]', description='Maximum current consumption in 2 mA steps (bMaxPower)', fmt='uint', value=50), 'reserved_1': hwio.register.Bitfield(bits='[7]', description='reserved (bmAttributes)', fmt='uint', value=1), 'power_source': hwio.register.Bitfield(bits='[6]', description='Power source (bmAttributes)', fmt='uint', values={'bus': 0, 'self': 1}, value='bus'), 'remote_wakeup': hwio.register.Bitfield(bits='[5]', description='Remote wakeup (bmAttributes)', fmt='uint', values={'no': 0, 'yes': 1}, value='no'), 'reserved_0': hwio.register.Bitfield(bits='[4:0]', description='reserved (bmAttributes)', fmt='uint', value=0)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H', 'FT2232H']:
            self.registers['chip_cfg'] = hwio.register.Register(description='Chip configuration', address=bitstring.Bits('0x05'), length=16, bitfields={'reserved_1': hwio.register.Bitfield(bits='[15:4]', description='reserved', fmt='uint', value=0), 'use_ser_no': hwio.register.Bitfield(bits='[3]', description='Use serial number', fmt='uint', values={'no': 0, 'yes': 1}, value='no' if serial_number is None else 'yes'), 'suspend_pd': hwio.register.Bitfield(bits='[2]', description='Enable internal pull-downs on pins in suspend mode', fmt='uint', values={'no': 0, 'yes': 1}, value='no'), 'reserved_0': hwio.register.Bitfield(bits='[1:0]', description='reserved', fmt='uint', value=0)})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT4232H']:
            self.registers['chip_cfg'] = hwio.register.Register(description='Chip configuration', address=bitstring.Bits('0x05'), length=16, bitfields={'dd7_cfg': hwio.register.Bitfield(bits='[15]', description='Pin DD7 configuration', fmt='uint', values={'ri#': 0, 'txden': 1}, value='ri#'), 'cd7_cfg': hwio.register.Bitfield(bits='[14]', description='Pin CD7 configuration', fmt='uint', values={'ri#': 0, 'txden': 1}, value='ri#'), 'bd7_cfg': hwio.register.Bitfield(bits='[13]', description='Pin BD7 configuration', fmt='uint', values={'ri#': 0, 'txden': 1}, value='ri#'), 'ad7_cfg': hwio.register.Bitfield(bits='[12]', description='Pin AD7 configuration', fmt='uint', values={'ri#': 0, 'txden': 1}, value='ri#'), 'reserved_1': hwio.register.Bitfield(bits='[11:4]', description='reserved', fmt='uint', value=0), 'use_ser_no': hwio.register.Bitfield(bits='[3]', description='Use serial number', fmt='uint', values={'no': 0, 'yes': 1}, value='no' if serial_number is None else 'yes'), 'suspend_pd': hwio.register.Bitfield(bits='[2]', description='Enable internal pull-downs on pins in suspend mode', fmt='uint', values={'no': 0, 'yes': 1}, value='no'), 'reserved_0': hwio.register.Bitfield(bits='[1:0]', description='reserved', fmt='uint', value=0)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            self.registers['pin_cfg'] = hwio.register.Register(description='Pin configuration', address=bitstring.Bits('0x06'), length=16, bitfields={'reserved': hwio.register.Bitfield(bits='[15:8]', description='reserved', fmt='uint', value=0), 'port_ac_hyst': hwio.register.Bitfield(bits='[7]', description='Port AC input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_ac_slew': hwio.register.Bitfield(bits='[6]', description='Port AC output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_ac_drive': hwio.register.Bitfield(bits='[5:4]', description='Port AC output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_ad_hyst': hwio.register.Bitfield(bits='[3]', description='Port AD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_ad_slew': hwio.register.Bitfield(bits='[2]', description='Port AD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_ad_drive': hwio.register.Bitfield(bits='[1:0]', description='Port AD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive)})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT2232H']:
            self.registers['pin_cfg'] = hwio.register.Register(description='Pin configuration', address=bitstring.Bits('0x06'), length=16, bitfields={'port_bc_hyst': hwio.register.Bitfield(bits='[15]', description='Port BC input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_bc_slew': hwio.register.Bitfield(bits='[14]', description='Port BC output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_bc_drive': hwio.register.Bitfield(bits='[13:12]', description='Port BC output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_bd_hyst': hwio.register.Bitfield(bits='[11]', description='Port BD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_bd_slew': hwio.register.Bitfield(bits='[10]', description='Port BD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_bd_drive': hwio.register.Bitfield(bits='[9:8]', description='Port BD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_ac_hyst': hwio.register.Bitfield(bits='[7]', description='Port AC input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_ac_slew': hwio.register.Bitfield(bits='[6]', description='Port AC output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_ac_drive': hwio.register.Bitfield(bits='[5:4]', description='Port AC output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_ad_hyst': hwio.register.Bitfield(bits='[3]', description='Port AD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_ad_slew': hwio.register.Bitfield(bits='[2]', description='Port AD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_ad_drive': hwio.register.Bitfield(bits='[1:0]', description='Port AD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive)})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT4232H']:
            self.registers['pin_cfg'] = hwio.register.Register(description='Pin configuration', address=bitstring.Bits('0x06'), length=16, bitfields={'port_dd_hyst': hwio.register.Bitfield(bits='[15]', description='Port DD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_dd_slew': hwio.register.Bitfield(bits='[14]', description='Port DD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_dd_drive': hwio.register.Bitfield(bits='[13:12]', description='Port DD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_cd_hyst': hwio.register.Bitfield(bits='[11]', description='Port CD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_cd_slew': hwio.register.Bitfield(bits='[10]', description='Port CD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_cd_drive': hwio.register.Bitfield(bits='[9:8]', description='Port CD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_bd_hyst': hwio.register.Bitfield(bits='[7]', description='Port BD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_bd_slew': hwio.register.Bitfield(bits='[6]', description='Port BD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_bd_drive': hwio.register.Bitfield(bits='[5:4]', description='Port BD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive), 'port_ad_hyst': hwio.register.Bitfield(bits='[3]', description='Port AD input hysteresis', fmt='uint', values={'no': 0, 'yes': 1}, value=hysteresis), 'port_ad_slew': hwio.register.Bitfield(bits='[2]', description='Port AD output slew', fmt='uint', values={'fast': 0, 'slow': 1}, value=slew), 'port_ad_drive': hwio.register.Bitfield(bits='[1:0]', description='Port AD output drive', fmt='uint', values={'4 mA': 0, '8 mA': 1, '12 mA': 2, '16 mA': 3}, value=drive)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H', 'FT2232H', 'FT4232H']:
            self.registers['usb_mfg_cfg'] = hwio.register.Register(description='USB manufacturer string configuration', address=bitstring.Bits('0x07'), length=16, bitfields={'mfg_str_len': hwio.register.Bitfield(bits='[15:8]', description='Manufacturer string length (iManufacturer)', fmt='uint', value=mfg_str_len), 'mfg_str_addr': hwio.register.Bitfield(bits='[7:0]', description='Manufacturer string address (iManufacturer)', fmt='uint', value=mfg_str_addr)})
            self.registers['usb_prod_cfg'] = hwio.register.Register(description='USB product string configuration', address=bitstring.Bits('0x08'), length=16, bitfields={'prod_str_len': hwio.register.Bitfield(bits='[15:8]', description='Product string length (iProduct)', fmt='uint', value=prod_str_len), 'prod_str_addr': hwio.register.Bitfield(bits='[7:0]', description='Product string address (iProduct)', fmt='uint', value=prod_str_addr)})
            self.registers['usb_ser_no_cfg'] = hwio.register.Register(description='USB Serial Number string configuration', address=bitstring.Bits('0x09'), length=16, bitfields={'ser_no_str_len': hwio.register.Bitfield(bits='[15:8]', description='Serial Number string length (iSerialNumber)', fmt='uint', value=ser_no_str_len), 'ser_no_str_addr': hwio.register.Bitfield(bits='[7:0]', description='Serial Number string address (iSerialNumber)', fmt='uint', value=ser_no_str_addr)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            self.registers['pin_ac_3_0_cfg'] = hwio.register.Register(description='Pin AC[3:0] configuration', address=bitstring.Bits('0x0C'), length=16, bitfields={'ac3': hwio.register.Bitfield(bits='[15:12]', description='Pin AC3 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'txd_en': 9}, value='tristate_pu'), 'ac2': hwio.register.Bitfield(bits='[11:8]', description='Pin AC2 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'txd_en': 9}, value='tristate_pu'), 'ac1': hwio.register.Bitfield(bits='[7:4]', description='Pin AC1 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'txd_en': 9}, value='tristate_pu'), 'ac0': hwio.register.Bitfield(bits='[3:0]', description='Pin AC0 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'drive_high': 7, 'txd_en': 9, 'clk_30mhz': 10, 'clk_15mhz': 11, 'clk_7_5mhz': 12}, value='tristate_pu')})
            self.registers['pin_ac_7_4_cfg'] = hwio.register.Register(description='Pin AC[7:4] configuration', address=bitstring.Bits('0x0D'), length=16, bitfields={'ac7': hwio.register.Bitfield(bits='[15:12]', description='Pin AC7 configuration', fmt='uint', values={'tristate_pu': 0}, value='tristate_pu'), 'ac6': hwio.register.Bitfield(bits='[11:8]', description='Pin AC6 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'drive_high': 7, 'io_mode': 8, 'txd_en': 9, 'clk_30mhz': 10, 'clk_15mhz': 11, 'clk_7_5mhz': 12}, value='tristate_pu'), 'ac5': hwio.register.Bitfield(bits='[7:4]', description='Pin AC5 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'drive_high': 7, 'io_mode': 8, 'txd_en': 9, 'clk_30mhz': 10, 'clk_15mhz': 11, 'clk_7_5mhz': 12}, value='tristate_pu'), 'ac4': hwio.register.Bitfield(bits='[3:0]', description='Pin AC4 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'txd_en': 9}, value='tristate_pu')})
            self.registers['pin_ac_9_8_cfg'] = hwio.register.Register(description='Pin AC[9:8] configuration', address=bitstring.Bits('0x0E'), length=16, bitfields={'reserved': hwio.register.Bitfield(bits='[15:8]', description='reserved', fmt='uint', value=0), 'ac9': hwio.register.Bitfield(bits='[7:4]', description='Pin AC9 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'drive_high': 7, 'io_mode': 8, 'txd_en': 9, 'clk_30mhz': 10, 'clk_15mhz': 11, 'clk_7_5mhz': 12}, value='tristate_pu'), 'ac8': hwio.register.Bitfield(bits='[3:0]', description='Pin AC8 configuration', fmt='uint', values={'tristate_pu': 0, 'tx_led#': 1, 'rx_led#': 2, 'txrx_led#': 3, 'ready#': 4, 'suspend#': 5, 'drive_low': 6, 'drive_high': 7, 'io_mode': 8, 'txd_en': 9, 'clk_30mhz': 10, 'clk_15mhz': 11, 'clk_7_5mhz': 12}, value='tristate_pu')})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            self.registers['eeprom_type'] = hwio.register.Register(description='EEPROM type', address=bitstring.Bits('0x0F'), length=16, bitfields={'eeprom_type': hwio.register.Bitfield(bits='[15:0]', description='EEPROM type', fmt='uint', values={'x56': 86, 'x66': 102}, value=eeprom_type)})
        elif PRODUCT_IDS[self.owner.device.idProduct] in ['FT2232H', 'FT4232H']:
            self.registers['eeprom_type'] = hwio.register.Register(description='EEPROM type', address=bitstring.Bits('0x0C'), length=16, bitfields={'eeprom_type': hwio.register.Bitfield(bits='[15:0]', description='EEPROM type', fmt='uint', values={'x56': 86, 'x66': 102}, value=eeprom_type)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H']:
            self.registers['vreg_cfg'] = hwio.register.Register(description='Chip configuration', address=bitstring.Bits('0x45'), length=16, bitfields={'reserved_1': hwio.register.Bitfield(bits='[15:7]', description='reserved', fmt='uint', value=0), 'vreg_adjust': hwio.register.Bitfield(bits='[6:4]', description='Voltage regulator adjustment', fmt='uint', values={'default': 4}, value='default'), 'reserved_0': hwio.register.Bitfield(bits='[3:0]', description='reserved', fmt='uint', value=8)})
        if PRODUCT_IDS[self.owner.device.idProduct] in ['FT232H', 'FT2232H', 'FT4232H']:
            self.registers['eeprom_checksum'] = hwio.register.Register(description='EEPROM checksum', address=bitstring.Bits('0x7F'), length=16, bitfields={'eeprom_checksum': hwio.register.Bitfield(bits='[15:0]', description='EEPROM checksum', fmt='uint', value=0)})

    def program(self):
        """Program

        Parameter:
        None

        Return:
        None

        """
        logger.debug(f'{self.description}, program')
        data = [0] * self.eeprom_size
        for register in self.registers.values():
            for offset, word in enumerate(register.value.cut(16)):
                data[register.address.uint + offset] = word.uint
        checksum = bitstring.BitArray(uint=43690, length=16)
        for address in range(127):
            checksum ^= bitstring.BitArray(uint=data[address], length=16)
            checksum.rol(bits=1)
        self.registers['eeprom_checksum'].bitfields['eeprom_checksum'].value = checksum.uint
        data[self.registers['eeprom_checksum'].address.uint] = self.registers['eeprom_checksum'].bitfields['eeprom_checksum'].value
        self.owner.eeprom_program(address=0, data=data)
        logger.debug('OK')
        return None