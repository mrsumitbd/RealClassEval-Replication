import pytest
import snippet_278 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    set_0 = set()
    dumper_0 = module_0.Dumper(*set_0)
    assert f'{type(dumper_0).__module__}.{type(dumper_0).__qualname__}' == 'snippet_278.Dumper'
    dumper_0.dump(dumper_0, set_0)

def test_case_1():
    int_0 = -2270
    dumper_0 = module_0.Dumper()
    assert f'{type(dumper_0).__module__}.{type(dumper_0).__qualname__}' == 'snippet_278.Dumper'
    with pytest.raises(NotImplementedError):
        dumper_0.load(int_0, int_0)