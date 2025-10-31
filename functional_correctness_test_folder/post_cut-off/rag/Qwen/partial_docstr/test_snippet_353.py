import pytest
import snippet_353 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(none_type_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path is None
    none_type_1 = None
    j_s_o_n_session_serializer_1 = module_0.JSONSessionSerializer(none_type_1)
    assert f'{type(j_s_o_n_session_serializer_1).__module__}.{type(j_s_o_n_session_serializer_1).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_1.storage_path is None
    j_s_o_n_session_serializer_1.write(j_s_o_n_session_serializer_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(bool_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path is True
    set_0 = set()
    j_s_o_n_session_serializer_0.read(j_s_o_n_session_serializer_0, bool_0, set_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = ''
    bool_0 = False
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(bool_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path is False
    j_s_o_n_session_serializer_0.read(str_0, str_0, str_0)

def test_case_3():
    bytes_0 = b'\xf0'
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(bytes_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path == b'\xf0'

@pytest.mark.xfail(strict=True)
def test_case_4():
    float_0 = 111.98
    none_type_0 = None
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(none_type_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path is None
    j_s_o_n_session_serializer_0.read(float_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    bytes_0 = b'\xe2\xdd'
    str_0 = '\th+tv'
    complex_0 = -904.65233 - 158.10179j
    j_s_o_n_session_serializer_0 = module_0.JSONSessionSerializer(complex_0)
    assert f'{type(j_s_o_n_session_serializer_0).__module__}.{type(j_s_o_n_session_serializer_0).__qualname__}' == 'snippet_353.JSONSessionSerializer'
    assert j_s_o_n_session_serializer_0.storage_path == -904.65233 - 158.10179j
    j_s_o_n_session_serializer_0.delete(bytes_0, str_0, str_0)