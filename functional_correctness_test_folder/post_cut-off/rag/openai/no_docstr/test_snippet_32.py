import pytest
import snippet_32 as module_0
import claude_monitor.utils.time_utils as module_1

def test_case_0():
    none_type_0 = None
    usage_entry_mapper_0 = module_0.UsageEntryMapper(none_type_0, none_type_0)
    assert f'{type(usage_entry_mapper_0).__module__}.{type(usage_entry_mapper_0).__qualname__}' == 'snippet_32.UsageEntryMapper'
    assert usage_entry_mapper_0.pricing_calculator is None
    assert usage_entry_mapper_0.timezone_handler is None

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '*B,N849g*>p-X\nA'
    str_1 = 'X+p.m0CzR '
    list_0 = [str_1, str_1, str_1]
    dict_0 = {str_0: str_0, str_1: str_1, str_0: list_0}
    bytes_0 = b'\xc8\x85r\x8c\x07k\x17\xa8\xad\xa6\x86c\xc6*,8'
    timezone_handler_0 = module_1.TimezoneHandler()
    assert f'{type(timezone_handler_0).__module__}.{type(timezone_handler_0).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    assert f'{type(timezone_handler_0.default_tz).__module__}.{type(timezone_handler_0.default_tz).__qualname__}' == 'pytz.UTC'
    assert module_1.HAS_BABEL is True
    assert f'{type(module_1.logger).__module__}.{type(module_1.logger).__qualname__}' == 'logging.Logger'
    assert module_1.logger.filters == []
    assert module_1.logger.name == 'claude_monitor.utils.time_utils'
    assert module_1.logger.level == 0
    assert f'{type(module_1.logger.parent).__module__}.{type(module_1.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_1.logger.propagate is True
    assert module_1.logger.handlers == []
    assert module_1.logger.disabled is False
    assert f'{type(module_1.logger.manager).__module__}.{type(module_1.logger.manager).__qualname__}' == 'logging.Manager'
    usage_entry_mapper_0 = module_0.UsageEntryMapper(bytes_0, timezone_handler_0)
    assert f'{type(usage_entry_mapper_0).__module__}.{type(usage_entry_mapper_0).__qualname__}' == 'snippet_32.UsageEntryMapper'
    assert usage_entry_mapper_0.pricing_calculator == b'\xc8\x85r\x8c\x07k\x17\xa8\xad\xa6\x86c\xc6*,8'
    assert f'{type(usage_entry_mapper_0.timezone_handler).__module__}.{type(usage_entry_mapper_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_entry_mapper_0.map(dict_0, str_1)