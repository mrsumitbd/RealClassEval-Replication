import pytest
import snippet_200 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    str_0 = '6'
    dict_0 = {str_0: bool_0}
    event_interceptor_0 = module_0.EventInterceptor(bool_0, **dict_0)
    assert f'{type(event_interceptor_0).__module__}.{type(event_interceptor_0).__qualname__}' == 'snippet_200.EventInterceptor'
    assert event_interceptor_0.source is True
    assert event_interceptor_0.events == {'6': True}
    event_interceptor_0.__enter__()

def test_case_1():
    none_type_0 = None
    int_0 = 4302
    event_interceptor_0 = module_0.EventInterceptor(int_0)
    assert f'{type(event_interceptor_0).__module__}.{type(event_interceptor_0).__qualname__}' == 'snippet_200.EventInterceptor'
    assert event_interceptor_0.source == 4302
    assert event_interceptor_0.events == {}
    event_interceptor_0.__enter__()
    event_interceptor_0.__exit__(none_type_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    str_0 = 'H\nth2'
    str_1 = '\x0bKF5~?{kZ_D&^N!'
    str_2 = ''
    dict_0 = {str_0: none_type_0, str_1: str_1, str_2: none_type_0}
    event_interceptor_0 = module_0.EventInterceptor(none_type_0, **dict_0)
    assert f'{type(event_interceptor_0).__module__}.{type(event_interceptor_0).__qualname__}' == 'snippet_200.EventInterceptor'
    assert event_interceptor_0.source is None
    assert event_interceptor_0.events == {'H\nth2': None, '\x0bKF5~?{kZ_D&^N!': '\x0bKF5~?{kZ_D&^N!', '': None}
    event_interceptor_0.__exit__(none_type_0, none_type_0, none_type_0)

def test_case_3():
    bool_0 = False
    bool_1 = False
    dict_0 = {}
    event_interceptor_0 = module_0.EventInterceptor(bool_1, **dict_0)
    assert f'{type(event_interceptor_0).__module__}.{type(event_interceptor_0).__qualname__}' == 'snippet_200.EventInterceptor'
    assert event_interceptor_0.source is False
    assert event_interceptor_0.events == {}
    event_interceptor_0.__exit__(bool_0, bool_0, bool_0)