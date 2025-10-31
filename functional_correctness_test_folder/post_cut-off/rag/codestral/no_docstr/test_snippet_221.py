import pytest
import snippet_221 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\xdd_\xd7zs\xc2P\x0b\xb7I\xe6)\x89\xcc\xb1\x1eq\x8d'
    module_0.GitHubTokenPool(bytes_0)

def test_case_1():
    list_0 = []
    with pytest.raises(ValueError):
        module_0.GitHubTokenPool(list_0)