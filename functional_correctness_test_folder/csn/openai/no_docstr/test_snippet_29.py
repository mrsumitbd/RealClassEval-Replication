import pytest
import snippet_29 as module_0
import platform as module_1
import numpy as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    rectangle_bin_0 = module_0.RectangleBin(none_type_0)
    assert f'{type(module_0.RectangleBin.extents).__module__}.{type(module_0.RectangleBin.extents).__qualname__}' == 'builtins.property'
    rectangle_bin_0.insert(rectangle_bin_0, rectangle_bin_0)

def test_case_1():
    none_type_0 = None
    rectangle_bin_0 = module_0.RectangleBin(none_type_0)
    assert f'{type(module_0.RectangleBin.extents).__module__}.{type(module_0.RectangleBin.extents).__qualname__}' == 'builtins.property'

@pytest.mark.xfail(strict=True)
def test_case_2():
    var_0 = module_1.python_version_tuple()
    rectangle_bin_0 = module_0.RectangleBin(var_0)
    assert f'{type(module_0.RectangleBin.extents).__module__}.{type(module_0.RectangleBin.extents).__qualname__}' == 'builtins.property'
    rectangle_bin_0.insert(rectangle_bin_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    var_0 = module_1.python_version_tuple()
    rectangle_bin_0 = module_0.RectangleBin(var_0)
    assert f'{type(module_0.RectangleBin.extents).__module__}.{type(module_0.RectangleBin.extents).__qualname__}' == 'builtins.property'
    rectangle_bin_0.insert(var_0, rectangle_bin_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    var_0 = module_1.python_version_tuple()
    rectangle_bin_0 = module_0.RectangleBin(var_0)
    assert f'{type(module_0.RectangleBin.extents).__module__}.{type(module_0.RectangleBin.extents).__qualname__}' == 'builtins.property'
    var_1 = module_2.source(var_0)
    assert module_2.newaxis is None
    assert module_2.little_endian is True
    assert module_2.Inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_2.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_2.infty == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_2.Infinity == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert f'{type(module_2.False_).__module__}.{type(module_2.False_).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_2.True_).__module__}.{type(module_2.True_).__qualname__}' == 'numpy.bool_'
    assert module_2.CLIP == 0
    assert module_2.RAISE == 2
    assert module_2.WRAP == 1
    assert module_2.MAXDIMS == 32
    assert module_2.BUFSIZE == 8192
    assert module_2.ALLOW_THREADS == 1
    assert module_2.MAY_SHARE_BOUNDS == 0
    assert module_2.MAY_SHARE_EXACT == -1
    assert module_2.ERR_CALL == 3
    assert module_2.ERR_DEFAULT == 521
    assert module_2.ERR_IGNORE == 0
    assert module_2.ERR_LOG == 5
    assert module_2.ERR_PRINT == 4
    assert module_2.ERR_RAISE == 2
    assert module_2.ERR_WARN == 1
    assert module_2.FLOATING_POINT_SUPPORT == 1
    assert module_2.FPE_DIVIDEBYZERO == 1
    assert module_2.FPE_INVALID == 8
    assert module_2.FPE_OVERFLOW == 2
    assert module_2.FPE_UNDERFLOW == 4
    assert module_2.NINF == pytest.approx(-1e309, abs=0.01, rel=0.01)
    assert module_2.NZERO == pytest.approx(-0.0, abs=0.01, rel=0.01)
    assert module_2.PINF == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_2.PZERO == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_2.SHIFT_DIVIDEBYZERO == 0
    assert module_2.SHIFT_INVALID == 9
    assert module_2.SHIFT_OVERFLOW == 3
    assert module_2.SHIFT_UNDERFLOW == 6
    assert module_2.UFUNC_BUFSIZE_DEFAULT == 8192
    assert module_2.UFUNC_PYVALS_NAME == 'UFUNC_PYVALS'
    assert module_2.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_2.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_2.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_2.sctypeDict).__module__}.{type(module_2.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_2.sctypeDict) == 132
    assert f'{type(module_2.sctypes).__module__}.{type(module_2.sctypes).__qualname__}' == 'builtins.dict'
    assert len(module_2.sctypes) == 5
    assert f'{type(module_2.ScalarType).__module__}.{type(module_2.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_2.ScalarType) == 31
    assert f'{type(module_2.cast).__module__}.{type(module_2.cast).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.cast) == 24
    assert f'{type(module_2.nbytes).__module__}.{type(module_2.nbytes).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.nbytes) == 24
    assert module_2.typecodes == {'Character': 'c', 'Integer': 'bhilqp', 'UnsignedInteger': 'BHILQP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqpBHILQPefdgFDGSUVOMm'}
    assert module_2.tracemalloc_domain == 389047
    assert f'{type(module_2.mgrid).__module__}.{type(module_2.mgrid).__qualname__}' == 'numpy.lib.index_tricks.MGridClass'
    assert module_2.mgrid.sparse is False
    assert f'{type(module_2.ogrid).__module__}.{type(module_2.ogrid).__qualname__}' == 'numpy.lib.index_tricks.OGridClass'
    assert module_2.ogrid.sparse is True
    assert f'{type(module_2.r_).__module__}.{type(module_2.r_).__qualname__}' == 'numpy.lib.index_tricks.RClass'
    assert len(module_2.r_) == 0
    assert f'{type(module_2.c_).__module__}.{type(module_2.c_).__qualname__}' == 'numpy.lib.index_tricks.CClass'
    assert len(module_2.c_) == 0
    assert f'{type(module_2.s_).__module__}.{type(module_2.s_).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_2.s_.maketuple is False
    assert f'{type(module_2.index_exp).__module__}.{type(module_2.index_exp).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_2.index_exp.maketuple is True
    assert module_2.oldnumeric == 'removed'
    assert module_2.numarray == 'removed'
    rectangle_bin_0.insert(var_1, var_1)