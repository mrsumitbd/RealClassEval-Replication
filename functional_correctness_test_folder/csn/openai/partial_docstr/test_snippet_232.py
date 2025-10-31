import pytest
import snippet_232 as module_0
import numpy as module_1
import numpy.char as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    module_0.Order0Interp(bool_0, bool_0, bool_0, bool_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    module_0.Order0Interp(bool_0, bool_0, bool_0, bool_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    var_0 = module_1.__dir__()
    assert module_1.newaxis is None
    assert module_1.little_endian is True
    assert module_1.Inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_1.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_1.infty == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_1.Infinity == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert f'{type(module_1.False_).__module__}.{type(module_1.False_).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_1.True_).__module__}.{type(module_1.True_).__qualname__}' == 'numpy.bool_'
    assert module_1.CLIP == 0
    assert module_1.RAISE == 2
    assert module_1.WRAP == 1
    assert module_1.MAXDIMS == 32
    assert module_1.BUFSIZE == 8192
    assert module_1.ALLOW_THREADS == 1
    assert module_1.MAY_SHARE_BOUNDS == 0
    assert module_1.MAY_SHARE_EXACT == -1
    assert module_1.ERR_CALL == 3
    assert module_1.ERR_DEFAULT == 521
    assert module_1.ERR_IGNORE == 0
    assert module_1.ERR_LOG == 5
    assert module_1.ERR_PRINT == 4
    assert module_1.ERR_RAISE == 2
    assert module_1.ERR_WARN == 1
    assert module_1.FLOATING_POINT_SUPPORT == 1
    assert module_1.FPE_DIVIDEBYZERO == 1
    assert module_1.FPE_INVALID == 8
    assert module_1.FPE_OVERFLOW == 2
    assert module_1.FPE_UNDERFLOW == 4
    assert module_1.NINF == pytest.approx(-1e309, abs=0.01, rel=0.01)
    assert module_1.NZERO == pytest.approx(-0.0, abs=0.01, rel=0.01)
    assert module_1.PINF == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_1.PZERO == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_1.SHIFT_DIVIDEBYZERO == 0
    assert module_1.SHIFT_INVALID == 9
    assert module_1.SHIFT_OVERFLOW == 3
    assert module_1.SHIFT_UNDERFLOW == 6
    assert module_1.UFUNC_BUFSIZE_DEFAULT == 8192
    assert module_1.UFUNC_PYVALS_NAME == 'UFUNC_PYVALS'
    assert module_1.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_1.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_1.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_1.sctypeDict).__module__}.{type(module_1.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_1.sctypeDict) == 132
    assert f'{type(module_1.sctypes).__module__}.{type(module_1.sctypes).__qualname__}' == 'builtins.dict'
    assert len(module_1.sctypes) == 5
    assert f'{type(module_1.ScalarType).__module__}.{type(module_1.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_1.ScalarType) == 31
    assert f'{type(module_1.cast).__module__}.{type(module_1.cast).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_1.cast) == 24
    assert f'{type(module_1.nbytes).__module__}.{type(module_1.nbytes).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_1.nbytes) == 24
    assert module_1.typecodes == {'Character': 'c', 'Integer': 'bhilqp', 'UnsignedInteger': 'BHILQP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqpBHILQPefdgFDGSUVOMm'}
    assert module_1.tracemalloc_domain == 389047
    assert f'{type(module_1.mgrid).__module__}.{type(module_1.mgrid).__qualname__}' == 'numpy.lib.index_tricks.MGridClass'
    assert module_1.mgrid.sparse is False
    assert f'{type(module_1.ogrid).__module__}.{type(module_1.ogrid).__qualname__}' == 'numpy.lib.index_tricks.OGridClass'
    assert module_1.ogrid.sparse is True
    assert f'{type(module_1.r_).__module__}.{type(module_1.r_).__qualname__}' == 'numpy.lib.index_tricks.RClass'
    assert len(module_1.r_) == 0
    assert f'{type(module_1.c_).__module__}.{type(module_1.c_).__qualname__}' == 'numpy.lib.index_tricks.CClass'
    assert len(module_1.c_) == 0
    assert f'{type(module_1.s_).__module__}.{type(module_1.s_).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_1.s_.maketuple is False
    assert f'{type(module_1.index_exp).__module__}.{type(module_1.index_exp).__qualname__}' == 'numpy.lib.index_tricks.IndexExpression'
    assert module_1.index_exp.maketuple is True
    assert module_1.oldnumeric == 'removed'
    assert module_1.numarray == 'removed'
    var_1 = module_2.array(var_0, unicode=var_0)
    bool_0 = False
    module_0.Order0Interp(var_1, var_0, var_0, var_0, bool_0)

def test_case_3():
    set_0 = set()
    bool_0 = False
    module_0.Order0Interp(set_0, set_0, set_0, bool_0, bool_0)