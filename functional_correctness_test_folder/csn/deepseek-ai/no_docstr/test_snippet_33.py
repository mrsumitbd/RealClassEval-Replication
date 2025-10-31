import pytest
import snippet_33 as module_0

def test_case_0():
    bool_0 = False
    exception_handler_0 = module_0.ExceptionHandler()
    assert f'{type(exception_handler_0).__module__}.{type(exception_handler_0).__qualname__}' == 'snippet_33.ExceptionHandler'
    var_0 = exception_handler_0.wants(bool_0)
    assert var_0 is True

def test_case_1():
    exception_handler_0 = module_0.ExceptionHandler()
    assert f'{type(exception_handler_0).__module__}.{type(exception_handler_0).__qualname__}' == 'snippet_33.ExceptionHandler'
    with pytest.raises(NotImplementedError):
        exception_handler_0.handle(exception_handler_0)