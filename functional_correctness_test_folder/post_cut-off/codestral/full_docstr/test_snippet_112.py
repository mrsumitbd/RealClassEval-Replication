import pytest
import snippet_112 as module_0

def test_case_0():
    float_0 = -3660.6
    session_reset_handler_0 = module_0.SessionResetHandler(float_0)
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.log == pytest.approx(-3660.6, abs=0.01, rel=0.01)
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    session_reset_handler_0.get_reset_info()

def test_case_1():
    session_reset_handler_0 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None

def test_case_2():
    complex_0 = 3248 + 4180.31j
    session_reset_handler_0 = module_0.SessionResetHandler(complex_0)
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.log == 3248 + 4180.31j
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    bool_0 = session_reset_handler_0.is_reset_pending()
    assert bool_0 is False
    none_type_0 = None
    session_reset_handler_1 = module_0.SessionResetHandler(bool_0)
    assert f'{type(session_reset_handler_1).__module__}.{type(session_reset_handler_1).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_1.reset_pending is False
    assert session_reset_handler_1.reset_command is None
    assert session_reset_handler_1.reset_time is None
    none_type_1 = session_reset_handler_1.mark_reset_detected(none_type_0)
    assert session_reset_handler_1.reset_pending is True
    assert session_reset_handler_1.reset_time == pytest.approx(1758862412.543618, abs=0.01, rel=0.01)
    session_reset_handler_2 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_2).__module__}.{type(session_reset_handler_2).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_2.reset_pending is False
    assert session_reset_handler_2.reset_command is None
    assert session_reset_handler_2.reset_time is None
    session_reset_handler_0.get_reset_info()
    session_reset_handler_1.get_reset_info()
    session_reset_handler_2.clear_reset_state()
    session_reset_handler_3 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_3).__module__}.{type(session_reset_handler_3).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_3.reset_pending is False
    assert session_reset_handler_3.reset_command is None
    assert session_reset_handler_3.reset_time is None
    str_0 = ';~W\rudy;\\8=P$/0&D$'
    bool_1 = session_reset_handler_3.check_for_reset_command(str_0)
    assert bool_1 is False

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = '2/QN*2+KM&Lmit%Ku51x'
    none_type_0 = None
    session_reset_handler_0 = module_0.SessionResetHandler(none_type_0)
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    none_type_1 = session_reset_handler_0.mark_reset_detected(str_0)
    assert session_reset_handler_0.reset_pending is True
    assert session_reset_handler_0.reset_command == '2/QN*2+KM&Lmit%Ku51x'
    assert session_reset_handler_0.reset_time == pytest.approx(1758862412.548183, abs=0.01, rel=0.01)
    var_0 = session_reset_handler_0.find_reset_session_file(none_type_0, none_type_1)
    var_1 = session_reset_handler_0.find_reset_session_file(var_0, str_0)
    session_reset_handler_1 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_1).__module__}.{type(session_reset_handler_1).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_1.reset_pending is False
    assert session_reset_handler_1.reset_command is None
    assert session_reset_handler_1.reset_time is None
    session_reset_handler_1.clear_reset_state()
    session_reset_handler_0.find_reset_session_file(session_reset_handler_1, var_1)

def test_case_4():
    bytes_0 = b''
    none_type_0 = None
    session_reset_handler_0 = module_0.SessionResetHandler(none_type_0)
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    session_reset_handler_1 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_1).__module__}.{type(session_reset_handler_1).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_1.reset_pending is False
    assert session_reset_handler_1.reset_command is None
    assert session_reset_handler_1.reset_time is None
    float_0 = -1192.88686
    session_reset_handler_2 = module_0.SessionResetHandler(session_reset_handler_0)
    assert f'{type(session_reset_handler_2).__module__}.{type(session_reset_handler_2).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert f'{type(session_reset_handler_2.log).__module__}.{type(session_reset_handler_2.log).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_2.reset_pending is False
    assert session_reset_handler_2.reset_command is None
    assert session_reset_handler_2.reset_time is None
    session_reset_handler_2.find_reset_session_file(none_type_0, none_type_0, float_0)
    none_type_1 = session_reset_handler_1.mark_reset_detected(bytes_0)
    assert session_reset_handler_1.reset_pending is True
    assert session_reset_handler_1.reset_command == b''
    assert session_reset_handler_1.reset_time == pytest.approx(1758862412.552105, abs=0.01, rel=0.01)

@pytest.mark.xfail(strict=True)
def test_case_5():
    bool_0 = True
    session_reset_handler_0 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    session_reset_handler_0.check_for_reset_command(bool_0)

def test_case_6():
    str_0 = "'x(\x0c30cs<IDfpe(`\n"
    session_reset_handler_0 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    none_type_0 = session_reset_handler_0.mark_reset_detected(str_0)
    assert session_reset_handler_0.reset_pending is True
    assert session_reset_handler_0.reset_command == "'x(\x0c30cs<IDfpe(`\n"
    assert session_reset_handler_0.reset_time == pytest.approx(1758862412.5545018, abs=0.01, rel=0.01)

def test_case_7():
    session_reset_handler_0 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    bool_0 = session_reset_handler_0.is_reset_pending()
    assert bool_0 is False

def test_case_8():
    str_0 = 'N"N;f'
    float_0 = -2354.283
    tuple_0 = (str_0, float_0)
    session_reset_handler_0 = module_0.SessionResetHandler(tuple_0)
    assert f'{type(session_reset_handler_0).__module__}.{type(session_reset_handler_0).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert f'{type(session_reset_handler_0.log).__module__}.{type(session_reset_handler_0.log).__qualname__}' == 'builtins.tuple'
    assert len(session_reset_handler_0.log) == 2
    assert session_reset_handler_0.reset_pending is False
    assert session_reset_handler_0.reset_command is None
    assert session_reset_handler_0.reset_time is None
    session_reset_handler_1 = module_0.SessionResetHandler()
    assert f'{type(session_reset_handler_1).__module__}.{type(session_reset_handler_1).__qualname__}' == 'snippet_112.SessionResetHandler'
    assert session_reset_handler_1.reset_pending is False
    assert session_reset_handler_1.reset_command is None
    assert session_reset_handler_1.reset_time is None
    session_reset_handler_1.clear_reset_state()
    bool_0 = session_reset_handler_1.is_reset_pending()
    assert bool_0 is False