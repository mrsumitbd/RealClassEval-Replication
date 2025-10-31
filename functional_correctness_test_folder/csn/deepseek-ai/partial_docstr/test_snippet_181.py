import pytest
import snippet_181 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'Y'
    base_loader_0 = module_0.BaseLoader()
    assert f'{type(base_loader_0).__module__}.{type(base_loader_0).__qualname__}' == 'snippet_181.BaseLoader'
    assert module_0.qType == {'SPARQL': 'sparql', 'TPF': 'tpf', 'JSON': 'json'}
    base_loader_0.getTextForName(str_0)

def test_case_1():
    base_loader_0 = module_0.BaseLoader()
    assert f'{type(base_loader_0).__module__}.{type(base_loader_0).__qualname__}' == 'snippet_181.BaseLoader'
    assert module_0.qType == {'SPARQL': 'sparql', 'TPF': 'tpf', 'JSON': 'json'}
    with pytest.raises(NotImplementedError):
        base_loader_0.fetchFiles()