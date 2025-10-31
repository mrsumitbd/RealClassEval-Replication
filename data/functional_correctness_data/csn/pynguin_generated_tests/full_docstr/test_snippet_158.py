import pytest
import snippet_158 as module_0

def test_case_0():
    bytes_0 = b'\x1bR~\xd9\xd1\xc7\x0f\x10\xdb83'
    bool_0 = False
    i_encoder_0 = module_0.IEncoder()
    assert f'{type(i_encoder_0).__module__}.{type(i_encoder_0).__qualname__}' == 'snippet_158.IEncoder'
    with pytest.raises(NotImplementedError):
        i_encoder_0.fits(bool_0, bool_0, bool_0, bytes_0)

def test_case_1():
    i_encoder_0 = module_0.IEncoder()
    assert f'{type(i_encoder_0).__module__}.{type(i_encoder_0).__qualname__}' == 'snippet_158.IEncoder'
    bytes_0 = b''
    with pytest.raises(NotImplementedError):
        i_encoder_0.encode_span(bytes_0)

def test_case_2():
    bytes_0 = b'\xf1*\xd9\xa2dX\xab]S\x92'
    list_0 = [bytes_0, bytes_0]
    i_encoder_0 = module_0.IEncoder()
    assert f'{type(i_encoder_0).__module__}.{type(i_encoder_0).__qualname__}' == 'snippet_158.IEncoder'
    with pytest.raises(NotImplementedError):
        i_encoder_0.encode_queue(list_0)