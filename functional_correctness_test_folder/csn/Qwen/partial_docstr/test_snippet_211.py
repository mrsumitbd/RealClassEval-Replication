import pytest
import snippet_211 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    dict_0 = {}
    none_type_0 = None
    bool_0 = True
    bytes_0 = b'\xad\xeb\x8a\x1b\x83\xe1\x89ouw\x87\xfeB\xce'
    field_definition_0 = module_0.FieldDefinition(bool_0, bool_0, bool_0, bool_0, bool_0, bytes_0)
    assert f'{type(field_definition_0).__module__}.{type(field_definition_0).__qualname__}' == 'snippet_211.FieldDefinition'
    assert field_definition_0.name is True
    assert field_definition_0.typeStr is True
    assert field_definition_0.optional is True
    assert field_definition_0.mapSubject is True
    assert field_definition_0.mapPredicate is True
    assert field_definition_0.typeDSL == b'\xad\xeb\x8a\x1b\x83\xe1\x89ouw\x87\xfeB\xce'
    field_definition_0.writeDefinition(dict_0, dict_0, none_type_0, none_type_0)