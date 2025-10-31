import pytest
import snippet_216 as module_0

def test_case_0():
    none_type_0 = None
    with pytest.raises(ValueError):
        module_0.Config(none_type_0, output_dir=none_type_0, temperature=none_type_0, prompt=none_type_0)

def test_case_1():
    tuple_0 = ()
    bool_0 = True
    str_0 = 'ht}H4`S\x0co'
    with pytest.raises(ValueError):
        module_0.Config(tuple_0, bool_0, str_0)