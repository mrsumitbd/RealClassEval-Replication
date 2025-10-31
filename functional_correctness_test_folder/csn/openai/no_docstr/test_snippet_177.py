import pytest
import snippet_177 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "KMB<Xo'vVM^F8\n20"
    module_0.tracked_lru_cache(str_0)