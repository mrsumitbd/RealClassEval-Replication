import pytest
import snippet_364 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'
    str_0 = ''
    c_l_i_result_0 = module_0.CLIResult(str_0, bytes_0)
    assert f'{type(c_l_i_result_0).__module__}.{type(c_l_i_result_0).__qualname__}' == 'snippet_364.CLIResult'
    assert c_l_i_result_0.status == ''
    assert c_l_i_result_0.message == b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'
    assert c_l_i_result_0.data is None
    assert c_l_i_result_0.exit_code == 0
    assert module_0.CLIResult.data is None
    assert module_0.CLIResult.exit_code == 0
    c_l_i_result_0.to_dict()
    dict_0 = {bytes_0: bytes_0, bytes_0: bytes_0}
    c_l_i_result_1 = module_0.CLIResult(dict_0, dict_0, bytes_0)
    assert f'{type(c_l_i_result_1).__module__}.{type(c_l_i_result_1).__qualname__}' == 'snippet_364.CLIResult'
    assert c_l_i_result_1.status == {b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0': b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'}
    assert c_l_i_result_1.message == {b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0': b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'}
    assert c_l_i_result_1.data == b'\xa1\x9c\xcbj\xf4\xec\xa8\x94(\xd9\xa0'
    assert c_l_i_result_1.exit_code == 0
    c_l_i_result_1.to_dict()

def test_case_1():
    str_0 = '*c\x0by{Qr94<h*,'
    c_l_i_result_0 = module_0.CLIResult(str_0, str_0, exit_code=str_0)
    assert f'{type(c_l_i_result_0).__module__}.{type(c_l_i_result_0).__qualname__}' == 'snippet_364.CLIResult'
    assert c_l_i_result_0.status == '*c\x0by{Qr94<h*,'
    assert c_l_i_result_0.message == '*c\x0by{Qr94<h*,'
    assert c_l_i_result_0.data is None
    assert c_l_i_result_0.exit_code == '*c\x0by{Qr94<h*,'
    assert module_0.CLIResult.data is None
    assert module_0.CLIResult.exit_code == 0
    bool_0 = c_l_i_result_0.is_success()
    assert bool_0 is False
    c_l_i_result_0.to_dict()

def test_case_2():
    str_0 = 'bIVE%@@k&PY\x0cx#a@z5'
    str_1 = '\n'
    c_l_i_result_0 = module_0.CLIResult(str_0, str_1, exit_code=str_0)
    assert f'{type(c_l_i_result_0).__module__}.{type(c_l_i_result_0).__qualname__}' == 'snippet_364.CLIResult'
    assert c_l_i_result_0.status == 'bIVE%@@k&PY\x0cx#a@z5'
    assert c_l_i_result_0.message == '\n'
    assert c_l_i_result_0.data is None
    assert c_l_i_result_0.exit_code == 'bIVE%@@k&PY\x0cx#a@z5'
    assert module_0.CLIResult.data is None
    assert module_0.CLIResult.exit_code == 0
    bool_0 = c_l_i_result_0.is_success()
    assert bool_0 is False