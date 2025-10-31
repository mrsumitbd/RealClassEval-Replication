import pytest
import pyaes.util as module_0
import snippet_11 as module_1

def test_case_0():
    bytes_0 = b'4}\xba7EV\x83D'
    var_0 = module_0.append_PKCS7_padding(bytes_0)
    assert var_0 == b'4}\xba7EV\x83D\x08\x08\x08\x08\x08\x08\x08\x08'
    a_e_s_mode_c_t_r_0 = module_1.AESModeCTR(var_0, var_0)
    assert f'{type(a_e_s_mode_c_t_r_0).__module__}.{type(a_e_s_mode_c_t_r_0).__qualname__}' == 'snippet_11.AESModeCTR'

def test_case_1():
    float_0 = -1265.7
    with pytest.raises(AssertionError):
        module_1.AESModeCTR(float_0, float_0)

def test_case_2():
    bytes_0 = b'\xd4d\xfawP\t\xe9\x8f\xbe\xd2\xe8\xd8\x82t\xe0\xe4\x17\x13\xdc'
    var_0 = module_0.append_PKCS7_padding(bytes_0)
    assert var_0 == b'\xd4d\xfawP\t\xe9\x8f\xbe\xd2\xe8\xd8\x82t\xe0\xe4\x17\x13\xdc\r\r\r\r\r\r\r\r\r\r\r\r\r'
    with pytest.raises(AssertionError):
        module_1.AESModeCTR(var_0, var_0)

def test_case_3():
    bytes_0 = b'4}\xba7EV\x83D'
    var_0 = module_0.append_PKCS7_padding(bytes_0)
    assert var_0 == b'4}\xba7EV\x83D\x08\x08\x08\x08\x08\x08\x08\x08'
    a_e_s_mode_c_t_r_0 = module_1.AESModeCTR(var_0, var_0)
    assert f'{type(a_e_s_mode_c_t_r_0).__module__}.{type(a_e_s_mode_c_t_r_0).__qualname__}' == 'snippet_11.AESModeCTR'
    with pytest.raises(AssertionError):
        module_1.AESModeCTR(var_0, a_e_s_mode_c_t_r_0)

def test_case_4():
    bytes_0 = b'4}\xba7EV\x83D'
    var_0 = module_0.append_PKCS7_padding(bytes_0)
    assert var_0 == b'4}\xba7EV\x83D\x08\x08\x08\x08\x08\x08\x08\x08'
    a_e_s_mode_c_t_r_0 = module_1.AESModeCTR(var_0, var_0)
    assert f'{type(a_e_s_mode_c_t_r_0).__module__}.{type(a_e_s_mode_c_t_r_0).__qualname__}' == 'snippet_11.AESModeCTR'
    var_1 = a_e_s_mode_c_t_r_0.encrypt(bytes_0)
    assert var_1 == b'\xcc9\xb5\x99\x95\xf2 M'

def test_case_5():
    bytes_0 = b'$\x83\xc8K\xee\xc3'
    var_0 = module_0.append_PKCS7_padding(bytes_0)
    assert var_0 == b'$\x83\xc8K\xee\xc3\n\n\n\n\n\n\n\n\n\n'
    a_e_s_mode_c_t_r_0 = module_1.AESModeCTR(var_0, var_0)
    assert f'{type(a_e_s_mode_c_t_r_0).__module__}.{type(a_e_s_mode_c_t_r_0).__qualname__}' == 'snippet_11.AESModeCTR'
    var_1 = a_e_s_mode_c_t_r_0.decrypt(var_0)
    assert var_1 == b'>\xde\x03\x9bR\x8e\x93\xd36\xfb\x10\x96\xe8*\x873'