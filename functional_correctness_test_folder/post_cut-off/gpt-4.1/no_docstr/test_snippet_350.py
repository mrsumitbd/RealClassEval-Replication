import pytest
import snippet_350 as module_0

def test_case_0():
    str_0 = 'd"B\njVcT!XV\t8ENk]ysQ'
    int_0 = -373
    str_1 = 'R*LZcTh}&3U\\W/AQ'
    str_2 = '\x0c\\1~\tihuF3)l$L)W#^s\t'
    startup_profiler_0 = module_0.StartupProfiler()
    assert f'{type(startup_profiler_0).__module__}.{type(startup_profiler_0).__qualname__}' == 'snippet_350.StartupProfiler'
    assert startup_profiler_0.profile_data == []
    assert startup_profiler_0.start_time == pytest.approx(2163838.276186999, abs=0.01, rel=0.01)
    dict_0 = {str_0: int_0, str_0: int_0, str_1: int_0, str_2: int_0}
    startup_profiler_1 = module_0.StartupProfiler()
    assert f'{type(startup_profiler_1).__module__}.{type(startup_profiler_1).__qualname__}' == 'snippet_350.StartupProfiler'
    assert startup_profiler_1.profile_data == []
    assert startup_profiler_1.start_time == pytest.approx(2163838.277054866, abs=0.01, rel=0.01)
    startup_profiler_1.analyze_bottlenecks(dict_0)
    startup_profiler_2 = module_0.StartupProfiler()
    assert f'{type(startup_profiler_2).__module__}.{type(startup_profiler_2).__qualname__}' == 'snippet_350.StartupProfiler'
    assert startup_profiler_2.profile_data == []
    assert startup_profiler_2.start_time == pytest.approx(2163838.277744448, abs=0.01, rel=0.01)
    var_0 = startup_profiler_0.checkpoint(startup_profiler_2)
    assert f'{type(startup_profiler_0.profile_data).__module__}.{type(startup_profiler_0.profile_data).__qualname__}' == 'builtins.list'
    assert len(startup_profiler_0.profile_data) == 1
    startup_profiler_0.get_report()

def test_case_1():
    startup_profiler_0 = module_0.StartupProfiler()
    assert f'{type(startup_profiler_0).__module__}.{type(startup_profiler_0).__qualname__}' == 'snippet_350.StartupProfiler'
    assert startup_profiler_0.profile_data == []
    assert startup_profiler_0.start_time == pytest.approx(2163838.279456516, abs=0.01, rel=0.01)
    dict_0 = startup_profiler_0.get_report()
    startup_profiler_0.analyze_bottlenecks(dict_0)

def test_case_2():
    set_0 = set()
    startup_profiler_0 = module_0.StartupProfiler()
    assert f'{type(startup_profiler_0).__module__}.{type(startup_profiler_0).__qualname__}' == 'snippet_350.StartupProfiler'
    assert startup_profiler_0.profile_data == []
    assert startup_profiler_0.start_time == pytest.approx(2163838.280647282, abs=0.01, rel=0.01)
    startup_profiler_0.get_report()
    var_0 = startup_profiler_0.checkpoint(set_0)
    assert f'{type(startup_profiler_0.profile_data).__module__}.{type(startup_profiler_0.profile_data).__qualname__}' == 'builtins.list'
    assert len(startup_profiler_0.profile_data) == 1