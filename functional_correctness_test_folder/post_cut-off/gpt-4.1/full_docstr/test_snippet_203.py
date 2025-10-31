import pytest
import snippet_203 as module_0

def test_case_0():
    target_python_0 = module_0.TargetPython()
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    target_python_0.get_sorted_tags()

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    tuple_0 = (bool_0, bool_0)
    target_python_0 = module_0.TargetPython(py_version_info=tuple_0, implementation=bool_0)
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    target_python_0.get_sorted_tags()

def test_case_2():
    int_0 = -3880
    tuple_0 = (int_0, int_0)
    str_0 = '2)g@N'
    list_0 = [str_0]
    target_python_0 = module_0.TargetPython(list_0, implementation=str_0)
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    target_python_0.get_unsorted_tags()
    target_python_1 = module_0.TargetPython(py_version_info=tuple_0)
    assert f'{type(target_python_1).__module__}.{type(target_python_1).__qualname__}' == 'snippet_203.TargetPython'
    str_1 = target_python_1.format_given()
    assert str_1 == "version_info='-3880.-3880'"

def test_case_3():
    target_python_0 = module_0.TargetPython()
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    target_python_0.get_unsorted_tags()
    str_0 = target_python_0.format_given()
    assert str_0 == ''

def test_case_4():
    str_0 = 'L'
    target_python_0 = module_0.TargetPython(implementation=str_0)
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    str_1 = target_python_0.format_given()
    assert str_1 == "implementation='L'"
    target_python_0.get_unsorted_tags()
    target_python_0.get_unsorted_tags()
    target_python_0.get_sorted_tags()

def test_case_5():
    target_python_0 = module_0.TargetPython()
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    target_python_0.get_unsorted_tags()
    target_python_0.get_unsorted_tags()

def test_case_6():
    str_0 = 'o\rbSZag'
    str_1 = 'si01k5yz:kg5\x0c'
    str_2 = 'nPq6vd8\\\nm33^Znz&{1'
    list_0 = [str_0, str_0, str_1, str_2]
    target_python_0 = module_0.TargetPython(list_0, abis=list_0, implementation=str_1)
    assert f'{type(target_python_0).__module__}.{type(target_python_0).__qualname__}' == 'snippet_203.TargetPython'
    assert f'{type(module_0.TargetPython.abis).__module__}.{type(module_0.TargetPython.abis).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.implementation).__module__}.{type(module_0.TargetPython.implementation).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.platforms).__module__}.{type(module_0.TargetPython.platforms).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version).__module__}.{type(module_0.TargetPython.py_version).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.TargetPython.py_version_info).__module__}.{type(module_0.TargetPython.py_version_info).__qualname__}' == 'builtins.member_descriptor'
    str_3 = target_python_0.format_given()
    assert str_3 == "platforms=['o\\rbSZag', 'o\\rbSZag', 'si01k5yz:kg5\\x0c', 'nPq6vd8\\\\\\nm33^Znz&{1'] abis=['o\\rbSZag', 'o\\rbSZag', 'si01k5yz:kg5\\x0c', 'nPq6vd8\\\\\\nm33^Znz&{1'] implementation='si01k5yz:kg5\\x0c'"