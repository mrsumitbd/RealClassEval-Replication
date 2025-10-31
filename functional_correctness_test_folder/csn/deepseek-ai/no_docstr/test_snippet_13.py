import pytest
import snippet_13 as module_0
import collections as module_1
import numpy.ma.core as module_2
import numpy as module_3

def test_case_0():
    module_0.velocity()

def test_case_1():
    bytes_0 = b'\xf1\x8a\xcfG\xf8\xc4W\x9f\xb5\x0bJ\xea\xcf\x11!B\x01\t\xf2'
    counter_0 = module_1.Counter()
    assert f'{type(module_1.Counter.fromkeys).__module__}.{type(module_1.Counter.fromkeys).__qualname__}' == 'builtins.method'
    var_0 = counter_0.__missing__(bytes_0)
    module_0.velocity(var_0, Q=var_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    velocity_0 = module_0.velocity()
    var_0 = module_2.allequal(velocity_0, velocity_0)
    assert f'{type(module_2.nomask).__module__}.{type(module_2.nomask).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_2.default_filler).__module__}.{type(module_2.default_filler).__qualname__}' == 'builtins.dict'
    assert len(module_2.default_filler) == 35
    assert module_2.v == 'as'
    assert f'{type(module_2.max_filler).__module__}.{type(module_2.max_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.max_filler) == 24
    assert f'{type(module_2.min_filler).__module__}.{type(module_2.min_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.min_filler) == 24
    assert f'{type(module_2.ufunc_domain).__module__}.{type(module_2.ufunc_domain).__qualname__}' == 'builtins.dict'
    assert len(module_2.ufunc_domain) == 47
    assert f'{type(module_2.ufunc_fills).__module__}.{type(module_2.ufunc_fills).__qualname__}' == 'builtins.dict'
    assert len(module_2.ufunc_fills) == 47
    assert f'{type(module_2.masked_print_option).__module__}.{type(module_2.masked_print_option).__qualname__}' == 'numpy.ma.core._MaskedPrintOption'
    assert f'{type(module_2.masked).__module__}.{type(module_2.masked).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    assert f'{type(module_2.masked_singleton).__module__}.{type(module_2.masked_singleton).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    var_1 = velocity_0.simulate(var_0)
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
    velocity_0.__call__(velocity_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    velocity_0 = module_0.velocity()
    module_0.velocity(seed=velocity_0)

def test_case_4():
    velocity_0 = module_0.velocity()
    var_0 = module_2.allequal(velocity_0, velocity_0)
    assert f'{type(module_2.nomask).__module__}.{type(module_2.nomask).__qualname__}' == 'numpy.bool_'
    assert f'{type(module_2.default_filler).__module__}.{type(module_2.default_filler).__qualname__}' == 'builtins.dict'
    assert len(module_2.default_filler) == 35
    assert module_2.v == 'as'
    assert f'{type(module_2.max_filler).__module__}.{type(module_2.max_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.max_filler) == 24
    assert f'{type(module_2.min_filler).__module__}.{type(module_2.min_filler).__qualname__}' == 'numpy.core.numerictypes._typedict'
    assert len(module_2.min_filler) == 24
    assert f'{type(module_2.ufunc_domain).__module__}.{type(module_2.ufunc_domain).__qualname__}' == 'builtins.dict'
    assert len(module_2.ufunc_domain) == 47
    assert f'{type(module_2.ufunc_fills).__module__}.{type(module_2.ufunc_fills).__qualname__}' == 'builtins.dict'
    assert len(module_2.ufunc_fills) == 47
    assert f'{type(module_2.masked_print_option).__module__}.{type(module_2.masked_print_option).__qualname__}' == 'numpy.ma.core._MaskedPrintOption'
    assert f'{type(module_2.masked).__module__}.{type(module_2.masked).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    assert f'{type(module_2.masked_singleton).__module__}.{type(module_2.masked_singleton).__qualname__}' == 'numpy.ma.core.MaskedConstant'
    var_1 = velocity_0.simulate(var_0)
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