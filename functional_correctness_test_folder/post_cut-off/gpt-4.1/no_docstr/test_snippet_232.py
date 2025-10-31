import pytest
import snippet_232 as module_0

def test_case_0():
    list_0 = []
    stopwatch_0 = module_0.Stopwatch(*list_0)
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    var_0 = stopwatch_0.__enter__()
    assert stopwatch_0.is_running is True
    assert stopwatch_0.start_time == pytest.approx(2154141.276637011, abs=0.01, rel=0.01)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert var_0.is_running is True
    assert var_0.start_time == pytest.approx(2154141.276637011, abs=0.01, rel=0.01)
    var_0.start()

def test_case_1():
    stopwatch_0 = module_0.Stopwatch()
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    var_0 = stopwatch_0.start()
    assert stopwatch_0.is_running is True
    assert stopwatch_0.start_time == pytest.approx(2154141.278485229, abs=0.01, rel=0.01)

def test_case_2():
    stopwatch_0 = module_0.Stopwatch()
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    var_0 = stopwatch_0.start()
    assert stopwatch_0.is_running is True
    assert stopwatch_0.start_time == pytest.approx(2154141.279541471, abs=0.01, rel=0.01)
    var_1 = stopwatch_0.stop()
    assert stopwatch_0.is_running is False
    assert stopwatch_0.elapsed == pytest.approx(0.0004278239794075489, abs=0.01, rel=0.01)
    assert stopwatch_0.elapsed_string == '00:00:00.000'

def test_case_3():
    stopwatch_0 = module_0.Stopwatch()
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    none_type_0 = None
    stopwatch_0.__exit__(none_type_0, none_type_0, none_type_0)
    var_0 = stopwatch_0.reset()
    assert stopwatch_0.elapsed == 0
    assert stopwatch_0.is_running is False

def test_case_4():
    stopwatch_0 = module_0.Stopwatch()
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    var_0 = stopwatch_0.__enter__()
    assert stopwatch_0.is_running is True
    assert stopwatch_0.start_time == pytest.approx(2154141.284246384, abs=0.01, rel=0.01)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert var_0.is_running is True
    assert var_0.start_time == pytest.approx(2154141.284246384, abs=0.01, rel=0.01)
    var_1 = var_0.reset()
    assert stopwatch_0.is_running is False
    assert stopwatch_0.elapsed == 0
    assert var_0.is_running is False
    assert var_0.elapsed == 0

def test_case_5():
    stopwatch_0 = module_0.Stopwatch()
    assert f'{type(stopwatch_0).__module__}.{type(stopwatch_0).__qualname__}' == 'snippet_232.Stopwatch'
    assert module_0.Stopwatch.elapsed == 0
    assert module_0.Stopwatch.elapsed_string == '0:00:00'
    assert module_0.Stopwatch.is_running is False
    var_0 = stopwatch_0.reset()
    assert stopwatch_0.elapsed == 0
    assert stopwatch_0.is_running is False