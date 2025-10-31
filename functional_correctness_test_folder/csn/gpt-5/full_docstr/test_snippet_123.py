import pytest
import snippet_123 as module_0

def test_case_0():
    multiprocessing_string_i_o_0 = module_0.MultiprocessingStringIO()
    assert f'{type(multiprocessing_string_i_o_0).__module__}.{type(multiprocessing_string_i_o_0).__qualname__}' == 'snippet_123.MultiprocessingStringIO'
    assert f'{type(module_0.MultiprocessingStringIO.proxy).__module__}.{type(module_0.MultiprocessingStringIO.proxy).__qualname__}' == 'multiprocessing.managers.ListProxy'
    multiprocessing_string_i_o_0.getvalue()

def test_case_1():
    str_0 = '6R\x0c8e1Og\x0cE|\r!I?c'
    multiprocessing_string_i_o_0 = module_0.MultiprocessingStringIO()
    assert f'{type(multiprocessing_string_i_o_0).__module__}.{type(multiprocessing_string_i_o_0).__qualname__}' == 'snippet_123.MultiprocessingStringIO'
    assert f'{type(module_0.MultiprocessingStringIO.proxy).__module__}.{type(module_0.MultiprocessingStringIO.proxy).__qualname__}' == 'multiprocessing.managers.ListProxy'
    multiprocessing_string_i_o_0.writelines(str_0)

def test_case_2():
    dict_0 = {}
    multiprocessing_string_i_o_0 = module_0.MultiprocessingStringIO(**dict_0)
    assert f'{type(multiprocessing_string_i_o_0).__module__}.{type(multiprocessing_string_i_o_0).__qualname__}' == 'snippet_123.MultiprocessingStringIO'
    assert f'{type(module_0.MultiprocessingStringIO.proxy).__module__}.{type(module_0.MultiprocessingStringIO.proxy).__qualname__}' == 'multiprocessing.managers.ListProxy'
    assert len(module_0.MultiprocessingStringIO.proxy) == 80
    multiprocessing_string_i_o_0.writelines(dict_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b'x\x8f\xaa\x89\xb8\x01\x90\xed\x86\x0f\x94g\xc6\xa4'
    multiprocessing_string_i_o_0 = module_0.MultiprocessingStringIO()
    assert f'{type(multiprocessing_string_i_o_0).__module__}.{type(multiprocessing_string_i_o_0).__qualname__}' == 'snippet_123.MultiprocessingStringIO'
    assert f'{type(module_0.MultiprocessingStringIO.proxy).__module__}.{type(module_0.MultiprocessingStringIO.proxy).__qualname__}' == 'multiprocessing.managers.ListProxy'
    assert len(module_0.MultiprocessingStringIO.proxy) == 80
    multiprocessing_string_i_o_0.write(bytes_0)