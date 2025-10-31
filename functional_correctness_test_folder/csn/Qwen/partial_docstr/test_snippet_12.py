import pytest
import snippet_12 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    factorization_0 = module_0.Factorization()
    assert f'{type(factorization_0).__module__}.{type(factorization_0).__qualname__}' == 'snippet_12.Factorization'
    assert f'{type(module_0.Factorization.factorize).__module__}.{type(module_0.Factorization.factorize).__qualname__}' == 'builtins.method'
    str_0 = 'w~4$h&VrmuErfL'
    factorization_0.gcd(str_0, str_0)

def test_case_1():
    factorization_0 = module_0.Factorization()
    assert f'{type(factorization_0).__module__}.{type(factorization_0).__qualname__}' == 'snippet_12.Factorization'
    assert f'{type(module_0.Factorization.factorize).__module__}.{type(module_0.Factorization.factorize).__qualname__}' == 'builtins.method'
    none_type_0 = None
    var_0 = factorization_0.gcd(factorization_0, none_type_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_12.Factorization'

def test_case_2():
    factorization_0 = module_0.Factorization()
    assert f'{type(factorization_0).__module__}.{type(factorization_0).__qualname__}' == 'snippet_12.Factorization'
    assert f'{type(module_0.Factorization.factorize).__module__}.{type(module_0.Factorization.factorize).__qualname__}' == 'builtins.method'
    int_0 = -3165
    var_0 = factorization_0.gcd(int_0, int_0)
    assert var_0 == -3165

@pytest.mark.xfail(strict=True)
def test_case_3():
    factorization_0 = module_0.Factorization()
    assert f'{type(factorization_0).__module__}.{type(factorization_0).__qualname__}' == 'snippet_12.Factorization'
    assert f'{type(module_0.Factorization.factorize).__module__}.{type(module_0.Factorization.factorize).__qualname__}' == 'builtins.method'
    bytes_0 = b'\x17\x0c\x19<\x85\x03@R#U\xea\x08'
    dict_0 = {bytes_0: bytes_0, bytes_0: bytes_0, bytes_0: bytes_0, bytes_0: bytes_0}
    factorization_0.gcd(bytes_0, dict_0)