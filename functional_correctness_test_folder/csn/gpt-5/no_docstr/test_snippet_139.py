import pytest
import snippet_139 as module_0

def test_case_0():
    none_type_0 = None
    lazy_field_0 = module_0.LazyField(none_type_0)
    assert f'{type(lazy_field_0).__module__}.{type(lazy_field_0).__qualname__}' == 'snippet_139.LazyField'
    assert lazy_field_0.klass is None
    assert lazy_field_0.kw == {}
    assert lazy_field_0.args == ()
    assert lazy_field_0.called is False
    lazy_field_1 = lazy_field_0.__call__()
    assert f'{type(lazy_field_1).__module__}.{type(lazy_field_1).__qualname__}' == 'snippet_139.LazyField'
    assert lazy_field_1.klass is None
    assert lazy_field_1.kw == {}
    assert lazy_field_1.args == ()
    assert lazy_field_1.called is False

def test_case_1():
    bytes_0 = b'\x17}f\xa0\xdfpX>\x88l'
    lazy_field_0 = module_0.LazyField(bytes_0)
    assert f'{type(lazy_field_0).__module__}.{type(lazy_field_0).__qualname__}' == 'snippet_139.LazyField'
    assert lazy_field_0.klass == b'\x17}f\xa0\xdfpX>\x88l'
    assert lazy_field_0.kw == {}
    assert lazy_field_0.args == ()
    assert lazy_field_0.called is False
    assert lazy_field_0.counter == 3247
    assert module_0.LazyField.counter == 3247
    lazy_field_1 = lazy_field_0.update()
    assert f'{type(lazy_field_1).__module__}.{type(lazy_field_1).__qualname__}' == 'snippet_139.LazyField'
    assert lazy_field_1.klass == b'\x17}f\xa0\xdfpX>\x88l'
    assert lazy_field_1.kw == {}
    assert lazy_field_1.args == ()
    assert lazy_field_1.called is False
    assert lazy_field_1.counter == 3247

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'\x17\xa0\xdfpX>\x88l'
    lazy_field_0 = module_0.LazyField(bytes_0)
    assert f'{type(lazy_field_0).__module__}.{type(lazy_field_0).__qualname__}' == 'snippet_139.LazyField'
    assert lazy_field_0.klass == b'\x17\xa0\xdfpX>\x88l'
    assert lazy_field_0.kw == {}
    assert lazy_field_0.args == ()
    assert lazy_field_0.called is False
    lazy_field_0.create()