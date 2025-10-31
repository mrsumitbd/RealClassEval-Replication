import pytest
import snippet_269 as module_0

def test_case_0():
    str_0 = 'd{O`9+TMfH)'
    field_0 = module_0.Field(str_0, str_0)
    assert f'{type(field_0).__module__}.{type(field_0).__qualname__}' == 'snippet_269.Field'
    assert field_0.sql_type == 'd{O`9+TMfH)'
    assert field_0.primary_key == 'd{O`9+TMfH)'
    assert field_0.nullable is True
    assert field_0.default is None
    assert field_0.name == ''
    str_1 = field_0.ddl()
    assert str_1 == ' d{O`9+TMfH) PRIMARY KEY'

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    field_0 = module_0.Field(none_type_0, none_type_0)
    assert f'{type(field_0).__module__}.{type(field_0).__qualname__}' == 'snippet_269.Field'
    assert field_0.sql_type is None
    assert field_0.primary_key is None
    assert field_0.nullable is True
    assert field_0.default is None
    assert field_0.name == ''
    field_0.ddl()

@pytest.mark.xfail(strict=True)
def test_case_2():
    dict_0 = {}
    bool_0 = False
    field_0 = module_0.Field(dict_0, nullable=bool_0)
    assert f'{type(field_0).__module__}.{type(field_0).__qualname__}' == 'snippet_269.Field'
    assert field_0.sql_type == {}
    assert field_0.primary_key is False
    assert field_0.nullable is False
    assert field_0.default is None
    assert field_0.name == ''
    field_0.ddl()

@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b'u#tR*[M\xdb'
    field_0 = module_0.Field(bytes_0, default=bytes_0)
    assert f'{type(field_0).__module__}.{type(field_0).__qualname__}' == 'snippet_269.Field'
    assert field_0.sql_type == b'u#tR*[M\xdb'
    assert field_0.primary_key is False
    assert field_0.nullable is True
    assert field_0.default == b'u#tR*[M\xdb'
    assert field_0.name == ''
    field_0.ddl()

def test_case_4():
    bool_0 = True
    field_0 = module_0.Field(bool_0, nullable=bool_0)
    assert f'{type(field_0).__module__}.{type(field_0).__qualname__}' == 'snippet_269.Field'
    assert field_0.sql_type is True
    assert field_0.primary_key is False
    assert field_0.nullable is True
    assert field_0.default is None
    assert field_0.name == ''