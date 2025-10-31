import pytest
import snippet_230 as module_0

def test_case_0():
    bool_0 = True
    raw_packet_0 = module_0.RawPacket(bool_0)
    assert f'{type(raw_packet_0).__module__}.{type(raw_packet_0).__qualname__}' == 'snippet_230.RawPacket'

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = -3648
    int_1 = 3618
    raw_packet_0 = module_0.RawPacket(int_1)
    assert f'{type(raw_packet_0).__module__}.{type(raw_packet_0).__qualname__}' == 'snippet_230.RawPacket'
    raw_packet_1 = module_0.RawPacket(raw_packet_0)
    assert f'{type(raw_packet_1).__module__}.{type(raw_packet_1).__qualname__}' == 'snippet_230.RawPacket'
    raw_packet_1.__getattr__(int_0)