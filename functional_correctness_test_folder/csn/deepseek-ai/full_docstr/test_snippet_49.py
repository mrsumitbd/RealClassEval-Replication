import pytest
import snippet_49 as module_0

def test_case_0():
    quil_atom_0 = module_0.QuilAtom()
    assert f'{type(quil_atom_0).__module__}.{type(quil_atom_0).__qualname__}' == 'snippet_49.QuilAtom'
    with pytest.raises(NotImplementedError):
        quil_atom_0.out()

def test_case_1():
    quil_atom_0 = module_0.QuilAtom()
    assert f'{type(quil_atom_0).__module__}.{type(quil_atom_0).__qualname__}' == 'snippet_49.QuilAtom'
    with pytest.raises(NotImplementedError):
        quil_atom_0.__str__()

def test_case_2():
    float_0 = -281.0
    quil_atom_0 = module_0.QuilAtom()
    assert f'{type(quil_atom_0).__module__}.{type(quil_atom_0).__qualname__}' == 'snippet_49.QuilAtom'
    with pytest.raises(NotImplementedError):
        quil_atom_0.__eq__(float_0)

def test_case_3():
    quil_atom_0 = module_0.QuilAtom()
    assert f'{type(quil_atom_0).__module__}.{type(quil_atom_0).__qualname__}' == 'snippet_49.QuilAtom'
    with pytest.raises(NotImplementedError):
        quil_atom_0.__hash__()