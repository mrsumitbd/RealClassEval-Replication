import pytest
import snippet_297 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'F\x16\xfd\xfd'
    module_0.Publish(bytes_0, aliases=bytes_0, broadcast_interval=bytes_0)