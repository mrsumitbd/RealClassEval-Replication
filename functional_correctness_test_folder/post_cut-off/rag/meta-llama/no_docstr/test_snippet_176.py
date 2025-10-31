import pytest
import snippet_176 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    circular_buffer_0 = module_0.CircularBuffer(none_type_0)
    assert f'{type(module_0.CircularBuffer.is_full).__module__}.{type(module_0.CircularBuffer.is_full).__qualname__}' == 'builtins.property'
    tensor_0 = circular_buffer_0.get_array()
    circular_buffer_0.append(tensor_0)

def test_case_1():
    int_0 = 2378
    circular_buffer_0 = module_0.CircularBuffer(int_0)
    assert f'{type(module_0.CircularBuffer.is_full).__module__}.{type(module_0.CircularBuffer.is_full).__qualname__}' == 'builtins.property'
    circular_buffer_0.get_array()

def test_case_2():
    bool_0 = False
    circular_buffer_0 = module_0.CircularBuffer(bool_0)
    assert f'{type(module_0.CircularBuffer.is_full).__module__}.{type(module_0.CircularBuffer.is_full).__qualname__}' == 'builtins.property'

def test_case_3():
    none_type_0 = None
    int_0 = 2342
    circular_buffer_0 = module_0.CircularBuffer(int_0, none_type_0)
    assert f'{type(module_0.CircularBuffer.is_full).__module__}.{type(module_0.CircularBuffer.is_full).__qualname__}' == 'builtins.property'
    tensor_0 = circular_buffer_0.get_array()
    circular_buffer_0.append(tensor_0)

def test_case_4():
    none_type_0 = None
    int_0 = 2342
    circular_buffer_0 = module_0.CircularBuffer(int_0, none_type_0)
    assert f'{type(module_0.CircularBuffer.is_full).__module__}.{type(module_0.CircularBuffer.is_full).__qualname__}' == 'builtins.property'
    tensor_0 = circular_buffer_0.get_array()
    tensor_1 = circular_buffer_0.get_array()
    circular_buffer_0.append(tensor_1)
    circular_buffer_0.append(tensor_0)