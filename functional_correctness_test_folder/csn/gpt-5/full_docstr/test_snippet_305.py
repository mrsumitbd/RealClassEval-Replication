import pytest
import snippet_305 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    quota_base_0 = module_0.QuotaBase()
    assert f'{type(quota_base_0).__module__}.{type(quota_base_0).__qualname__}' == 'snippet_305.QuotaBase'
    quota_base_0.get_quota_usage()