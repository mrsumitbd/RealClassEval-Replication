import pytest
import snippet_206 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\xe4\xf8\xd8\x02\xed\xe9\xccYq\xd6uA\x0f\xde'
    str_0 = '(LKb"6(}9gl04'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.write_hex_file(bytes_0, str_0, bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    str_0 = '#uAOwj\r.,_PO/,o[T55@'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.write_hex_file(bool_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    str_0 = 'E'
    bytes_0 = b'\x97\x17B\xbe`\x1d\xc9\x06'
    bool_0 = False
    config_space_hex_formatter_0.write_hex_file(bytes_0, str_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'E'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.validate_hex_file(str_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = 'a,F~Tn=?}'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.validate_hex_file(str_0)

def test_case_5():
    bytes_0 = b'-\x01\x82\x91\x05\xa0^/\xa3\xb0\xee\xeb#\xb2.\x9a\xcd6'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.convert_to_dword_list(bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = 'lP<gPw;M'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.convert_to_dword_list(str_0)

def test_case_7():
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}

@pytest.mark.xfail(strict=True)
def test_case_8():
    bytes_0 = b'\xf1\xe6c\xf4'
    str_0 = 'E'
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    config_space_hex_formatter_0.write_hex_file(bytes_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    config_space_hex_formatter_0 = module_0.ConfigSpaceHexFormatter()
    assert f'{type(config_space_hex_formatter_0).__module__}.{type(config_space_hex_formatter_0).__qualname__}' == 'snippet_206.ConfigSpaceHexFormatter'
    assert f'{type(config_space_hex_formatter_0.logger).__module__}.{type(config_space_hex_formatter_0.logger).__qualname__}' == 'logging.Logger'
    assert module_0.ConfigSpaceHexFormatter.REGISTER_NAMES == {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}
    str_0 = ''
    config_space_hex_formatter_0.validate_hex_file(str_0)