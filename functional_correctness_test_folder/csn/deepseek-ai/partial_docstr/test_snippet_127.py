import pytest
import snippet_127 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\x9a\xd6\x17\x8d\xbb}\x901~\x9c\xbb\xb0\x1f'
    module_0.LowestCommonAncestorShortcuts(bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '<'
    module_0.LowestCommonAncestorShortcuts(str_0)