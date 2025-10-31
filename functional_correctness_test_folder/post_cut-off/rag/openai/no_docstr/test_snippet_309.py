import pytest
import snippet_309 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = -539
    module_0.LocalFileBlobStore(int_0, int_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    module_0.LocalFileBlobStore()