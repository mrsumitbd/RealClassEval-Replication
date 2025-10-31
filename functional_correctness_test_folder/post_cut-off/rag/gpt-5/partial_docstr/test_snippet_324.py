import pytest
import snippet_324 as module_0

def test_case_0():
    bool_0 = True
    command_rate_limiter_0 = module_0.CommandRateLimiter(bool_0)
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls is True
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    int_0 = command_rate_limiter_0.calls_remaining()
    assert int_0 == 1
    bool_1 = command_rate_limiter_0.can_call()
    assert bool_1 is True
    assert f'{type(command_rate_limiter_0.calls).__module__}.{type(command_rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_0.calls) == 1
    bool_2 = command_rate_limiter_0.can_call()
    assert bool_2 is False
    float_0 = command_rate_limiter_0.time_to_next_call()
    assert float_0 == pytest.approx(59.99939298629761, abs=0.01, rel=0.01)

def test_case_1():
    bool_0 = True
    command_rate_limiter_0 = module_0.CommandRateLimiter(bool_0)
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls is True
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    bool_1 = command_rate_limiter_0.can_call()
    assert bool_1 is True
    assert f'{type(command_rate_limiter_0.calls).__module__}.{type(command_rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_0.calls) == 1

def test_case_2():
    command_rate_limiter_0 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls == 5
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    int_0 = command_rate_limiter_0.calls_remaining()
    assert int_0 == 5
    command_rate_limiter_1 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_1).__module__}.{type(command_rate_limiter_1).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_1.calls == []
    assert command_rate_limiter_1.max_calls == 5
    assert command_rate_limiter_1.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    bool_0 = command_rate_limiter_1.can_call()
    assert bool_0 is True
    assert f'{type(command_rate_limiter_1.calls).__module__}.{type(command_rate_limiter_1.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_1.calls) == 1
    bool_1 = command_rate_limiter_1.can_call()
    assert bool_1 is True
    assert len(command_rate_limiter_1.calls) == 2

def test_case_3():
    command_rate_limiter_0 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls == 5
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    float_0 = command_rate_limiter_0.time_to_next_call()
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)
    command_rate_limiter_1 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_1).__module__}.{type(command_rate_limiter_1).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_1.calls == []
    assert command_rate_limiter_1.max_calls == 5
    assert command_rate_limiter_1.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    bool_0 = command_rate_limiter_1.can_call()
    assert bool_0 is True
    assert f'{type(command_rate_limiter_1.calls).__module__}.{type(command_rate_limiter_1.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_1.calls) == 1
    int_0 = command_rate_limiter_1.calls_remaining()
    assert int_0 == 4

def test_case_4():
    command_rate_limiter_0 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls == 5
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    bool_0 = command_rate_limiter_0.can_call()
    assert bool_0 is True
    assert f'{type(command_rate_limiter_0.calls).__module__}.{type(command_rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_0.calls) == 1
    float_0 = command_rate_limiter_0.time_to_next_call()
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)
    int_0 = -1161
    command_rate_limiter_1 = module_0.CommandRateLimiter(int_0)
    assert f'{type(command_rate_limiter_1).__module__}.{type(command_rate_limiter_1).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_1.calls == []
    assert command_rate_limiter_1.max_calls == -1161
    assert command_rate_limiter_1.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    int_1 = command_rate_limiter_1.calls_remaining()
    assert int_1 == 0

def test_case_5():
    command_rate_limiter_0 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls == 5
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)

def test_case_6():
    command_rate_limiter_0 = module_0.CommandRateLimiter()
    assert f'{type(command_rate_limiter_0).__module__}.{type(command_rate_limiter_0).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_0.calls == []
    assert command_rate_limiter_0.max_calls == 5
    assert command_rate_limiter_0.period == pytest.approx(60.0, abs=0.01, rel=0.01)
    bool_0 = False
    bool_1 = command_rate_limiter_0.can_call()
    assert bool_1 is True
    assert f'{type(command_rate_limiter_0.calls).__module__}.{type(command_rate_limiter_0.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_0.calls) == 1
    float_0 = command_rate_limiter_0.time_to_next_call()
    assert float_0 == pytest.approx(0.0, abs=0.01, rel=0.01)
    bool_2 = command_rate_limiter_0.can_call()
    assert bool_2 is True
    assert len(command_rate_limiter_0.calls) == 2
    int_0 = command_rate_limiter_0.calls_remaining()
    assert int_0 == 3
    command_rate_limiter_1 = module_0.CommandRateLimiter(period=bool_0)
    assert f'{type(command_rate_limiter_1).__module__}.{type(command_rate_limiter_1).__qualname__}' == 'snippet_324.CommandRateLimiter'
    assert command_rate_limiter_1.calls == []
    assert command_rate_limiter_1.max_calls == 5
    assert command_rate_limiter_1.period is False
    bool_3 = command_rate_limiter_1.can_call()
    assert bool_3 is True
    assert f'{type(command_rate_limiter_1.calls).__module__}.{type(command_rate_limiter_1.calls).__qualname__}' == 'builtins.list'
    assert len(command_rate_limiter_1.calls) == 1
    bool_4 = command_rate_limiter_1.can_call()
    assert bool_4 is True
    int_1 = command_rate_limiter_1.calls_remaining()
    assert int_1 == 5
    assert command_rate_limiter_1.calls == []