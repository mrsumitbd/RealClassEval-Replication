import pytest
import snippet_35 as module_0

def test_case_0():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None
    with pytest.raises(Exception):
        timer___0.tac()

def test_case_1():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None
    timer___0.tic()
    timer___0.toc(timer___0)
    timer___0.tac()

def test_case_2():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None
    with pytest.raises(Exception):
        timer___0.toc()

def test_case_3():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None

def test_case_4():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None
    var_0 = timer___0.tic()
    var_1 = timer___0.tac()
    timer___0.toc(var_0, var_1)
    timer___0.toc()

def test_case_5():
    timer___0 = module_0.__Timer__()
    assert module_0.__Timer__.start is None
    assert module_0.__Timer__.last is None
    var_0 = timer___0.tic()
    timer___0.tac(var_0)
    timer___0.tac()