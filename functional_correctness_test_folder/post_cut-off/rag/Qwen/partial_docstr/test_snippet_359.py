import pytest
import snippet_359 as module_0
import numpy as module_1

def test_case_0():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    d_r_f_p_util_0.shingling_from_mol(d_r_f_p_util_0, include_hydrogens=d_r_f_p_util_0)

def test_case_1():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    bool_0 = True
    bool_1 = True
    str_0 = '~DlDFx,`JW)QS#xn,;5'
    with pytest.raises(ValueError):
        d_r_f_p_util_0.internal_encode(str_0, bool_0, rings=bool_1, root_central_atom=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    int_0 = 1101
    bool_0 = True
    d_r_f_p_util_0.encode(d_r_f_p_util_0, int_0, atom_index_mapping=bool_0, include_hydrogens=d_r_f_p_util_0)

def test_case_3():
    list_0 = []
    d_r_f_p_util_0 = module_0.DRFPUtil()
    int_0 = 1101
    bool_0 = True
    none_type_0 = None
    d_r_f_p_util_0.encode(list_0, radius=int_0, rings=bool_0, atom_index_mapping=none_type_0, include_hydrogens=bool_0)

def test_case_4():
    module_0.DRFPUtil()

@pytest.mark.xfail(strict=True)
def test_case_5():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    var_0 = d_r_f_p_util_0.__repr__()
    d_r_f_p_util_0.encode(var_0, min_radius=var_0, atom_index_mapping=var_0, show_progress_bar=var_0)

def test_case_6():
    list_0 = []
    d_r_f_p_util_0 = module_0.DRFPUtil()
    int_0 = 1101
    bool_0 = False
    none_type_0 = None
    d_r_f_p_util_0.fold(int_0)
    d_r_f_p_util_0.encode(list_0, radius=int_0, rings=bool_0, atom_index_mapping=none_type_0, include_hydrogens=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    str_0 = 'C='
    var_0 = d_r_f_p_util_0.__repr__()
    bool_0 = False
    d_r_f_p_util_0.encode(var_0, min_radius=var_0, atom_index_mapping=bool_0, show_progress_bar=str_0)

def test_case_8():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    d_r_f_p_util_0.shingling_from_mol(d_r_f_p_util_0, d_r_f_p_util_0)

def test_case_9():
    list_0 = []
    d_r_f_p_util_0 = module_0.DRFPUtil()
    ndarray_0 = d_r_f_p_util_0.hash(list_0)
    assert f'{type(module_1.ndarray.ndim).__module__}.{type(module_1.ndarray.ndim).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.flags).__module__}.{type(module_1.ndarray.flags).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.shape).__module__}.{type(module_1.ndarray.shape).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.strides).__module__}.{type(module_1.ndarray.strides).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.data).__module__}.{type(module_1.ndarray.data).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.itemsize).__module__}.{type(module_1.ndarray.itemsize).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.size).__module__}.{type(module_1.ndarray.size).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.nbytes).__module__}.{type(module_1.ndarray.nbytes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.base).__module__}.{type(module_1.ndarray.base).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.dtype).__module__}.{type(module_1.ndarray.dtype).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.real).__module__}.{type(module_1.ndarray.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.imag).__module__}.{type(module_1.ndarray.imag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.flat).__module__}.{type(module_1.ndarray.flat).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.ctypes).__module__}.{type(module_1.ndarray.ctypes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.T).__module__}.{type(module_1.ndarray.T).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.mT).__module__}.{type(module_1.ndarray.mT).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.ptp).__module__}.{type(module_1.ndarray.ptp).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.newbyteorder).__module__}.{type(module_1.ndarray.newbyteorder).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.itemset).__module__}.{type(module_1.ndarray.itemset).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.ndarray.device).__module__}.{type(module_1.ndarray.device).__qualname__}' == 'builtins.getset_descriptor'
    int_0 = 1101
    bool_0 = True
    none_type_0 = None
    var_0 = d_r_f_p_util_0.encode(list_0, radius=int_0, rings=bool_0, atom_index_mapping=none_type_0, include_hydrogens=bool_0)
    assert f'{type(module_1.False_).__module__}.{type(module_1.False_).__qualname__}' == 'numpy.bool'
    assert f'{type(module_1.ScalarType).__module__}.{type(module_1.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_1.ScalarType) == 31
    assert f'{type(module_1.True_).__module__}.{type(module_1.True_).__qualname__}' == 'numpy.bool'
    assert module_1.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_1.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_1.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_1.little_endian is True
    assert module_1.newaxis is None
    assert module_1.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_1.sctypeDict).__module__}.{type(module_1.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_1.sctypeDict) == 52
    assert module_1.typecodes == {'Character': 'c', 'Integer': 'bhilqnp', 'UnsignedInteger': 'BHILQNP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQnNpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqnpBHILQNPefdgFDGSUVOMm'}
    assert f'{type(module_1.c_).__module__}.{type(module_1.c_).__qualname__}' == 'numpy.lib._index_tricks_impl.CClass'
    assert len(module_1.c_) == 0
    assert f'{type(module_1.r_).__module__}.{type(module_1.r_).__qualname__}' == 'numpy.lib._index_tricks_impl.RClass'
    assert len(module_1.r_) == 0
    assert f'{type(module_1.s_).__module__}.{type(module_1.s_).__qualname__}' == 'numpy.lib._index_tricks_impl.IndexExpression'
    assert f'{type(module_1.ogrid).__module__}.{type(module_1.ogrid).__qualname__}' == 'numpy.lib._index_tricks_impl.OGridClass'
    assert f'{type(module_1.mgrid).__module__}.{type(module_1.mgrid).__qualname__}' == 'numpy.lib._index_tricks_impl.MGridClass'
    assert f'{type(module_1.index_exp).__module__}.{type(module_1.index_exp).__qualname__}' == 'numpy.lib._index_tricks_impl.IndexExpression'

@pytest.mark.xfail(strict=True)
def test_case_10():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    str_0 = '$7\tnkh8@A2g`kQ4'
    list_0 = [str_0]
    d_r_f_p_util_0.hash(list_0)

@pytest.mark.xfail(strict=True)
def test_case_11():
    d_r_f_p_util_0 = module_0.DRFPUtil()
    none_type_0 = None
    bool_0 = False
    bool_1 = False
    d_r_f_p_util_0.shingling_from_mol(none_type_0, bool_0, bool_1, bool_0)