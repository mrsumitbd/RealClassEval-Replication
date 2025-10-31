import snippet_285 as module_0

def test_case_0():
    str_0 = '>L.is'
    block_0 = module_0.Block(str_0, str_0, str_0)
    assert f'{type(block_0).__module__}.{type(block_0).__qualname__}' == 'snippet_285.Block'
    assert block_0.block_type == '>L.is'
    assert block_0.content == '>L.is'
    assert block_0.title == '>L.is'
    str_1 = block_0.__repr__()
    assert str_1 == 'Block(type=>L.is, title=>L.is)'
    bytes_0 = b'\x08\x05\xf6\x9aX\xcb\x1d\x18&\xac9'
    str_2 = 'QLDM{@EpO,N`jRxt5W?'
    block_1 = module_0.Block(bytes_0, str_2)
    assert f'{type(block_1).__module__}.{type(block_1).__qualname__}' == 'snippet_285.Block'
    assert block_1.block_type == b'\x08\x05\xf6\x9aX\xcb\x1d\x18&\xac9'
    assert block_1.content == 'QLDM{@EpO,N`jRxt5W?'
    assert block_1.title is None
    str_3 = block_1.__repr__()
    assert str_3 == "Block(type=b'\\x08\\x05\\xf6\\x9aX\\xcb\\x1d\\x18&\\xac9')"

def test_case_1():
    str_0 = 's4]hUi:~g#'
    str_1 = '{J.fP&e2m;EH*T9\t'
    block_0 = module_0.Block(str_0, str_1)
    assert f'{type(block_0).__module__}.{type(block_0).__qualname__}' == 'snippet_285.Block'
    assert block_0.block_type == 's4]hUi:~g#'
    assert block_0.content == '{J.fP&e2m;EH*T9\t'
    assert block_0.title is None
    str_2 = block_0.__repr__()
    assert str_2 == 'Block(type=s4]hUi:~g#)'

def test_case_2():
    int_0 = 1190
    block_0 = module_0.Block(int_0, int_0)
    assert f'{type(block_0).__module__}.{type(block_0).__qualname__}' == 'snippet_285.Block'
    assert block_0.block_type == 1190
    assert block_0.content == 1190
    assert block_0.title is None