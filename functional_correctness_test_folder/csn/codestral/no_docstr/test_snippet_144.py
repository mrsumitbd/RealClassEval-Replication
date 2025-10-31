import pytest
import snippet_144 as module_0

def test_case_0():
    in_given_directory_0 = module_0.InGivenDirectory()
    assert f'{type(in_given_directory_0).__module__}.{type(in_given_directory_0).__qualname__}' == 'snippet_144.InGivenDirectory'

@pytest.mark.xfail(strict=True)
def test_case_1():
    tuple_0 = ()
    module_0.InGivenDirectory(tuple_0)

def test_case_2():
    in_given_directory_0 = module_0.InGivenDirectory()
    assert f'{type(in_given_directory_0).__module__}.{type(in_given_directory_0).__qualname__}' == 'snippet_144.InGivenDirectory'
    in_given_directory_0.__enter__()

def test_case_3():
    str_0 = '1(xop,nZV.9hzl`'
    in_given_directory_0 = module_0.InGivenDirectory(str_0)
    assert f'{type(in_given_directory_0).__module__}.{type(in_given_directory_0).__qualname__}' == 'snippet_144.InGivenDirectory'
    in_given_directory_0.__enter__()
    in_given_directory_1 = module_0.InGivenDirectory()
    assert f'{type(in_given_directory_1).__module__}.{type(in_given_directory_1).__qualname__}' == 'snippet_144.InGivenDirectory'
    in_given_directory_1.__enter__()

@pytest.mark.xfail(strict=True)
def test_case_4():
    in_given_directory_0 = module_0.InGivenDirectory()
    assert f'{type(in_given_directory_0).__module__}.{type(in_given_directory_0).__qualname__}' == 'snippet_144.InGivenDirectory'
    in_given_directory_1 = module_0.InGivenDirectory()
    assert f'{type(in_given_directory_1).__module__}.{type(in_given_directory_1).__qualname__}' == 'snippet_144.InGivenDirectory'
    in_given_directory_1.__exit__(in_given_directory_0, in_given_directory_0, in_given_directory_0)