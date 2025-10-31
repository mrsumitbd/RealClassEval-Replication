import pytest
import platform as module_0
import numpy.ma.core as module_1
import snippet_203 as module_2
import numpy as module_3
import numpy.polynomial.hermite_e as module_4

def test_case_0():
    module_0.python_branch()

@pytest.mark.xfail(strict=True)
def test_case_1():
    list_0 = []
    masked_constant_0 = module_1.MaskedConstant(*list_0)
    assert f'{type(module_1.nomask).__module__}.{type(module_1.nomask).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_1.default_filler).__module__}.{type(module_1.default_filler).__qualname__}' == 'builtins.dict'
    assert len(module_1.default_filler) == 35
    assert module_1.v == 'as'
    assert f'{type(module_1.max_filler).__module__}.{type(module_1.max_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_1.max_filler) == 24
    assert f'{type(module_1.min_filler).__module__}.{type(module_1.min_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_1.min_filler) == 24
    assert f'{type(module_1.ufunc_domain).__module__}.{type(module_1.ufunc_domain).__qualname__}' == 'builtins.dict'
    assert len(module_1.ufunc_domain) == 47
    assert f'{type(module_1.ufunc_fills).__module__}.{type(module_1.ufunc_fills).__qualname__}' == 'builtins.dict'
    assert len(module_1.ufunc_fills) == 47
    assert f'{type(module_1.masked_print_option).__module__}.{type(module_1.masked_print_option).__qualname__}' == 'numpy.ma.core._MaskedPrintOption'
    assert f'{type(module_1.masked).__module__}.{type(module_1.masked).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    assert f'{type(module_1.masked_singleton).__module__}.{type(module_1.masked_singleton).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    none_type_0 = None
    module_2.MegKDE(masked_constant_0, factor=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    var_0 = module_3.asmatrix(none_type_0)
    assert module_3.newaxis is None
    assert module_3.little_endian is True
    assert module_3.Inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.infty == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.Infinity == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert f'{type(module_3.False_).__module__}.{type(module_3.False_).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_3.True_).__module__}.{type(module_3.True_).__qualname__}' == 'numpy.bool_'
    assert module_3.CLIP == 0
    assert module_3.RAISE == 2
    assert module_3.WRAP == 1
    assert module_3.MAXDIMS == 32
    assert module_3.BUFSIZE == 8192
    assert module_3.ALLOW_THREADS == 1
    assert module_3.MAY_SHARE_BOUNDS == 0
    assert module_3.MAY_SHARE_EXACT == -1
    assert module_3.ERR_CALL == 3
    assert module_3.ERR_DEFAULT == 521
    assert module_3.ERR_IGNORE == 0
    assert module_3.ERR_LOG == 5
    assert module_3.ERR_PRINT == 4
    assert module_3.ERR_RAISE == 2
    assert module_3.ERR_WARN == 1
    assert module_3.FLOATING_POINT_SUPPORT == 1
    assert module_3.FPE_DIVIDEBYZERO == 1
    assert module_3.FPE_INVALID == 8
    assert module_3.FPE_OVERFLOW == 2
    assert module_3.FPE_UNDERFLOW == 4
    assert module_3.NINF == pytest.approx(-1e309, abs=0.01, rel=0.01)
    assert module_3.NZERO == pytest.approx(-0.0, abs=0.01, rel=0.01)
    assert module_3.PINF == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.PZERO == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_3.SHIFT_DIVIDEBYZERO == 0
    assert module_3.SHIFT_INVALID == 9
    assert module_3.SHIFT_OVERFLOW == 3
    assert module_3.SHIFT_UNDERFLOW == 6
    assert module_3.UFUNC_BUFSIZE_DEFAULT == 8192
    assert module_3.UFUNC_PYVALS_NAME == 'UFUNC_PYVALS'
    assert module_3.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_3.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_3.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_3.sctypeDict).__module__}.{type(module_3.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_3.sctypeDict) == 132
    assert f'{type(module_3.sctypes).__module__}.{type(module_3.sctypes).__qualname__}' == 'builtins.dict'
    assert len(module_3.sctypes) == 5
    assert f'{type(module_3.ScalarType).__module__}.{type(module_3.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_3.ScalarType) == 31
    assert f'{type(module_3.cast).__module__}.{type(module_3.cast).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_3.cast) == 24
    assert f'{type(module_3.nbytes).__module__}.{type(module_3.nbytes).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_3.nbytes) == 24
    assert module_3.typecodes == {'Character': 'c', 'Integer': 'bhilqp', 'UnsignedInteger': 'BHILQP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqpBHILQPefdgFDGSUVOMm'}
    assert module_3.tracemalloc_domain == 389047
    assert f'{type(module_3.mgrid).__module__}.{type(module_3.mgrid).__qualname__}' == 'numpy.lib.index_tricks.MGridClass'
    assert module_3.mgrid.sparse is False
    assert f'{type(module_3.ogrid).__module__}.{type(module_3.ogrid).__qualname__}' == 'numpy.lib.index_tricks.OGridClass'
    assert module_3.ogrid.sparse is True
    assert f'{type(module_3.r_).__module__}.{type(module_3.r_).__qualname__}' == 'numpy.lib.index_tricks.RClass'
    assert len(module_3.r_) == 0
    assert f'{type(module_3.c_).__module__}.{type(module_3.c_).__qualname__}' == 'numpy.lib.index_tricks.CClass'
    assert len(module_3.c_) == 0
    assert f'{type(module_3.s_).__module__}.{type(module_3.s_).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_3.s_.maketuple is False
    assert f'{type(module_3.index_exp).__module__}.{type(module_3.index_exp).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_3.index_exp.maketuple is True
    assert module_3.oldnumeric == 'removed'
    assert module_3.numarray == 'removed'
    assert f'{type(module_3.matrix.I).__module__}.{type(module_3.matrix.I).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.A).__module__}.{type(module_3.matrix.A).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.A1).__module__}.{type(module_3.matrix.A1).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.T).__module__}.{type(module_3.matrix.T).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.H).__module__}.{type(module_3.matrix.H).__qualname__}' == 'builtins.property'
    module_2.MegKDE(var_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    var_0 = module_3.asmatrix(none_type_0)
    assert module_3.newaxis is None
    assert module_3.little_endian is True
    assert module_3.Inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.infty == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.Infinity == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert f'{type(module_3.False_).__module__}.{type(module_3.False_).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_3.True_).__module__}.{type(module_3.True_).__qualname__}' == 'numpy.bool_'
    assert module_3.CLIP == 0
    assert module_3.RAISE == 2
    assert module_3.WRAP == 1
    assert module_3.MAXDIMS == 32
    assert module_3.BUFSIZE == 8192
    assert module_3.ALLOW_THREADS == 1
    assert module_3.MAY_SHARE_BOUNDS == 0
    assert module_3.MAY_SHARE_EXACT == -1
    assert module_3.ERR_CALL == 3
    assert module_3.ERR_DEFAULT == 521
    assert module_3.ERR_IGNORE == 0
    assert module_3.ERR_LOG == 5
    assert module_3.ERR_PRINT == 4
    assert module_3.ERR_RAISE == 2
    assert module_3.ERR_WARN == 1
    assert module_3.FLOATING_POINT_SUPPORT == 1
    assert module_3.FPE_DIVIDEBYZERO == 1
    assert module_3.FPE_INVALID == 8
    assert module_3.FPE_OVERFLOW == 2
    assert module_3.FPE_UNDERFLOW == 4
    assert module_3.NINF == pytest.approx(-1e309, abs=0.01, rel=0.01)
    assert module_3.NZERO == pytest.approx(-0.0, abs=0.01, rel=0.01)
    assert module_3.PINF == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_3.PZERO == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_3.SHIFT_DIVIDEBYZERO == 0
    assert module_3.SHIFT_INVALID == 9
    assert module_3.SHIFT_OVERFLOW == 3
    assert module_3.SHIFT_UNDERFLOW == 6
    assert module_3.UFUNC_BUFSIZE_DEFAULT == 8192
    assert module_3.UFUNC_PYVALS_NAME == 'UFUNC_PYVALS'
    assert module_3.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_3.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_3.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_3.sctypeDict).__module__}.{type(module_3.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_3.sctypeDict) == 132
    assert f'{type(module_3.sctypes).__module__}.{type(module_3.sctypes).__qualname__}' == 'builtins.dict'
    assert len(module_3.sctypes) == 5
    assert f'{type(module_3.ScalarType).__module__}.{type(module_3.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_3.ScalarType) == 31
    assert f'{type(module_3.cast).__module__}.{type(module_3.cast).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_3.cast) == 24
    assert f'{type(module_3.nbytes).__module__}.{type(module_3.nbytes).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_3.nbytes) == 24
    assert module_3.typecodes == {'Character': 'c', 'Integer': 'bhilqp', 'UnsignedInteger': 'BHILQP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqpBHILQPefdgFDGSUVOMm'}
    assert module_3.tracemalloc_domain == 389047
    assert f'{type(module_3.mgrid).__module__}.{type(module_3.mgrid).__qualname__}' == 'numpy.lib.index_tricks.MGridClass'
    assert module_3.mgrid.sparse is False
    assert f'{type(module_3.ogrid).__module__}.{type(module_3.ogrid).__qualname__}' == 'numpy.lib.index_tricks.OGridClass'
    assert module_3.ogrid.sparse is True
    assert f'{type(module_3.r_).__module__}.{type(module_3.r_).__qualname__}' == 'numpy.lib.index_tricks.RClass'
    assert len(module_3.r_) == 0
    assert f'{type(module_3.c_).__module__}.{type(module_3.c_).__qualname__}' == 'numpy.lib.index_tricks.CClass'
    assert len(module_3.c_) == 0
    assert f'{type(module_3.s_).__module__}.{type(module_3.s_).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_3.s_.maketuple is False
    assert f'{type(module_3.index_exp).__module__}.{type(module_3.index_exp).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_3.index_exp.maketuple is True
    assert module_3.oldnumeric == 'removed'
    assert module_3.numarray == 'removed'
    assert f'{type(module_3.matrix.I).__module__}.{type(module_3.matrix.I).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.A).__module__}.{type(module_3.matrix.A).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.A1).__module__}.{type(module_3.matrix.A1).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.T).__module__}.{type(module_3.matrix.T).__qualname__}' == 'builtins.property'
    assert f'{type(module_3.matrix.H).__module__}.{type(module_3.matrix.H).__qualname__}' == 'builtins.property'
    module_2.MegKDE(var_0, var_0, nmin=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    none_type_0 = None
    var_0 = module_4.herme2poly(none_type_0)
    assert f'{type(module_4.hermedomain).__module__}.{type(module_4.hermedomain).__qualname__}' == 'numpy.ndarray'
    assert len(module_4.hermedomain) == 2
    assert f'{type(module_4.hermezero).__module__}.{type(module_4.hermezero).__qualname__}' == 'numpy.ndarray'
    assert len(module_4.hermezero) == 1
    assert f'{type(module_4.hermeone).__module__}.{type(module_4.hermeone).__qualname__}' == 'numpy.ndarray'
    assert len(module_4.hermeone) == 1
    assert f'{type(module_4.hermex).__module__}.{type(module_4.hermex).__qualname__}' == 'numpy.ndarray'
    assert len(module_4.hermex) == 2
    assert f'{type(module_3.ndarray.ndim).__module__}.{type(module_3.ndarray.ndim).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.flags).__module__}.{type(module_3.ndarray.flags).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.shape).__module__}.{type(module_3.ndarray.shape).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.strides).__module__}.{type(module_3.ndarray.strides).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.data).__module__}.{type(module_3.ndarray.data).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.itemsize).__module__}.{type(module_3.ndarray.itemsize).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.size).__module__}.{type(module_3.ndarray.size).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.nbytes).__module__}.{type(module_3.ndarray.nbytes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.base).__module__}.{type(module_3.ndarray.base).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.dtype).__module__}.{type(module_3.ndarray.dtype).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.real).__module__}.{type(module_3.ndarray.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.imag).__module__}.{type(module_3.ndarray.imag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.flat).__module__}.{type(module_3.ndarray.flat).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.ctypes).__module__}.{type(module_3.ndarray.ctypes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_3.ndarray.T).__module__}.{type(module_3.ndarray.T).__qualname__}' == 'builtins.getset_descriptor'
    module_2.MegKDE(var_0, nmin=none_type_0)