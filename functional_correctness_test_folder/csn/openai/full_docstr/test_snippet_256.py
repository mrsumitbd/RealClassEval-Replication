import snippet_256 as module_0
import numpy.lib.utils as module_1
import numpy as module_2

def test_case_0():
    variance_function_0 = module_0.VarianceFunction()
    var_0 = module_1.get_include()
    var_1 = variance_function_0.__call__(var_0)
    assert f'{type(module_2.ndarray.ndim).__module__}.{type(module_2.ndarray.ndim).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.flags).__module__}.{type(module_2.ndarray.flags).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.shape).__module__}.{type(module_2.ndarray.shape).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.strides).__module__}.{type(module_2.ndarray.strides).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.data).__module__}.{type(module_2.ndarray.data).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.itemsize).__module__}.{type(module_2.ndarray.itemsize).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.size).__module__}.{type(module_2.ndarray.size).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.nbytes).__module__}.{type(module_2.ndarray.nbytes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.base).__module__}.{type(module_2.ndarray.base).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.dtype).__module__}.{type(module_2.ndarray.dtype).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.real).__module__}.{type(module_2.ndarray.real).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.imag).__module__}.{type(module_2.ndarray.imag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.flat).__module__}.{type(module_2.ndarray.flat).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.ctypes).__module__}.{type(module_2.ndarray.ctypes).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_2.ndarray.T).__module__}.{type(module_2.ndarray.T).__qualname__}' == 'builtins.getset_descriptor'

def test_case_1():
    module_0.VarianceFunction()