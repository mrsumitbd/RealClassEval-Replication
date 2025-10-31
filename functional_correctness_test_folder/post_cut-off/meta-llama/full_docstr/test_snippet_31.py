import pytest
import snippet_31 as module_0
import claude_monitor.core.models as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    usage_aggregator_0 = module_0.UsageAggregator(none_type_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path is None
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    bytes_0 = b'\xc2e'
    usage_aggregator_0.aggregate_monthly(bytes_0, end_date=none_type_0)

def test_case_1():
    dict_0 = {}
    str_0 = "vD2j] D'j"
    usage_aggregator_0 = module_0.UsageAggregator(str_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == "vD2j] D'j"
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_aggregator_0.aggregate_monthly(dict_0)

def test_case_2():
    none_type_0 = None
    str_0 = '[\n&?Y?3\x0cukJMvR-sH&-'
    str_1 = '#15^Y^qmJAqN..E*'
    usage_aggregator_0 = module_0.UsageAggregator(str_1)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == '#15^Y^qmJAqN..E*'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    with pytest.raises(ValueError):
        usage_aggregator_0.aggregate_from_blocks(none_type_0, str_0)

def test_case_3():
    set_0 = set()
    usage_aggregator_0 = module_0.UsageAggregator(set_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == {*()}
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_aggregator_0.aggregate_from_blocks(set_0)

def test_case_4():
    str_0 = '?v1K:WxZ7M'
    usage_aggregator_0 = module_0.UsageAggregator(str_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == '?v1K:WxZ7M'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = 'xA;U\x0b*z'
    usage_aggregator_0 = module_0.UsageAggregator(str_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == 'xA;U\x0b*z'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    none_type_0 = None
    str_1 = "uN\\D?_#'MAZy\x0b-*#"
    usage_entry_0 = module_1.UsageEntry(str_0, none_type_0, usage_aggregator_0, cache_read_tokens=str_0, model=str_0, message_id=str_1)
    assert f'{type(usage_entry_0).__module__}.{type(usage_entry_0).__qualname__}' == 'claude_monitor.core.models.UsageEntry'
    assert usage_entry_0.timestamp == 'xA;U\x0b*z'
    assert usage_entry_0.input_tokens is None
    assert f'{type(usage_entry_0.output_tokens).__module__}.{type(usage_entry_0.output_tokens).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_entry_0.cache_creation_tokens == 0
    assert usage_entry_0.cache_read_tokens == 'xA;U\x0b*z'
    assert usage_entry_0.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert usage_entry_0.model == 'xA;U\x0b*z'
    assert usage_entry_0.message_id == "uN\\D?_#'MAZy\x0b-*#"
    assert usage_entry_0.request_id == ''
    assert module_1.UsageEntry.cache_creation_tokens == 0
    assert module_1.UsageEntry.cache_read_tokens == 0
    assert module_1.UsageEntry.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_1.UsageEntry.model == ''
    assert module_1.UsageEntry.message_id == ''
    assert module_1.UsageEntry.request_id == ''
    list_0 = [usage_entry_0, usage_entry_0, usage_entry_0]
    usage_aggregator_0.aggregate_daily(list_0, none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    int_0 = -1715
    list_0 = [int_0, int_0, int_0, int_0]
    usage_aggregator_0 = module_0.UsageAggregator(list_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == [-1715, -1715, -1715, -1715]
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_aggregator_0.aggregate_monthly(list_0, end_date=int_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    str_0 = 'K _)5R{Dff&.|s/#\x0b3~{'
    none_type_0 = None
    bool_0 = False
    bool_1 = False
    str_1 = 'S:;e'
    usage_aggregator_0 = module_0.UsageAggregator(str_1)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == 'S:;e'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_entry_0 = module_1.UsageEntry(bool_0, str_0, bool_1, request_id=str_0)
    assert f'{type(usage_entry_0).__module__}.{type(usage_entry_0).__qualname__}' == 'claude_monitor.core.models.UsageEntry'
    assert usage_entry_0.timestamp is False
    assert usage_entry_0.input_tokens == 'K _)5R{Dff&.|s/#\x0b3~{'
    assert usage_entry_0.output_tokens is False
    assert usage_entry_0.cache_creation_tokens == 0
    assert usage_entry_0.cache_read_tokens == 0
    assert usage_entry_0.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert usage_entry_0.model == ''
    assert usage_entry_0.message_id == ''
    assert usage_entry_0.request_id == 'K _)5R{Dff&.|s/#\x0b3~{'
    assert module_1.UsageEntry.cache_creation_tokens == 0
    assert module_1.UsageEntry.cache_read_tokens == 0
    assert module_1.UsageEntry.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_1.UsageEntry.model == ''
    assert module_1.UsageEntry.message_id == ''
    assert module_1.UsageEntry.request_id == ''
    list_0 = [usage_entry_0, usage_entry_0, usage_entry_0, usage_entry_0]
    usage_aggregator_0.aggregate_monthly(list_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_8():
    set_0 = set()
    usage_aggregator_0 = module_0.UsageAggregator(set_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == {*()}
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    usage_aggregator_0.aggregate_from_blocks(set_0)
    str_0 = 'Oz3Pf~'
    usage_aggregator_0.aggregate_from_blocks(str_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    str_0 = 'daily'
    usage_aggregator_0 = module_0.UsageAggregator(str_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == 'daily'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    str_1 = '\r$\tt6C`h^Y9Fp\nSy#>'
    none_type_0 = None
    list_0 = [str_0, str_0, str_1]
    session_block_0 = module_1.SessionBlock(str_1, usage_aggregator_0, usage_aggregator_0, token_counts=none_type_0, per_model_stats=none_type_0, models=list_0, projection_data=none_type_0)
    assert f'{type(session_block_0).__module__}.{type(session_block_0).__qualname__}' == 'claude_monitor.core.models.SessionBlock'
    assert session_block_0.id == '\r$\tt6C`h^Y9Fp\nSy#>'
    assert f'{type(session_block_0.start_time).__module__}.{type(session_block_0.start_time).__qualname__}' == 'snippet_31.UsageAggregator'
    assert f'{type(session_block_0.end_time).__module__}.{type(session_block_0.end_time).__qualname__}' == 'snippet_31.UsageAggregator'
    assert session_block_0.entries == []
    assert session_block_0.token_counts is None
    assert session_block_0.is_active is False
    assert session_block_0.is_gap is False
    assert session_block_0.burn_rate is None
    assert session_block_0.actual_end_time is None
    assert session_block_0.per_model_stats is None
    assert session_block_0.models == ['daily', 'daily', '\r$\tt6C`h^Y9Fp\nSy#>']
    assert session_block_0.sent_messages_count == 0
    assert session_block_0.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert session_block_0.limit_messages == []
    assert session_block_0.projection_data is None
    assert session_block_0.burn_rate_snapshot is None
    assert module_1.SessionBlock.is_active is False
    assert module_1.SessionBlock.is_gap is False
    assert module_1.SessionBlock.burn_rate is None
    assert module_1.SessionBlock.actual_end_time is None
    assert module_1.SessionBlock.sent_messages_count == 0
    assert module_1.SessionBlock.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_1.SessionBlock.projection_data is None
    assert module_1.SessionBlock.burn_rate_snapshot is None
    assert f'{type(module_1.SessionBlock.total_tokens).__module__}.{type(module_1.SessionBlock.total_tokens).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.SessionBlock.total_cost).__module__}.{type(module_1.SessionBlock.total_cost).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.SessionBlock.duration_minutes).__module__}.{type(module_1.SessionBlock.duration_minutes).__qualname__}' == 'builtins.property'
    var_0 = session_block_0.__repr__()
    var_1 = var_0.__eq__(str_0)
    assert var_1 is False
    list_1 = [session_block_0, session_block_0, var_1, session_block_0]
    usage_aggregator_0.aggregate_from_blocks(list_1)

@pytest.mark.xfail(strict=True)
def test_case_10():
    str_0 = 'xA;U\x0b*z'
    usage_aggregator_0 = module_0.UsageAggregator(str_0)
    assert f'{type(usage_aggregator_0).__module__}.{type(usage_aggregator_0).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_aggregator_0.data_path == 'xA;U\x0b*z'
    assert usage_aggregator_0.aggregation_mode == 'daily'
    assert usage_aggregator_0.timezone == 'UTC'
    assert f'{type(usage_aggregator_0.timezone_handler).__module__}.{type(usage_aggregator_0.timezone_handler).__qualname__}' == 'claude_monitor.utils.time_utils.TimezoneHandler'
    str_1 = "uN\\D?_#'MAZy\x0b-*#"
    usage_entry_0 = module_1.UsageEntry(str_0, str_1, usage_aggregator_0, cache_read_tokens=str_0, model=str_0, message_id=str_1)
    assert f'{type(usage_entry_0).__module__}.{type(usage_entry_0).__qualname__}' == 'claude_monitor.core.models.UsageEntry'
    assert usage_entry_0.timestamp == 'xA;U\x0b*z'
    assert usage_entry_0.input_tokens == "uN\\D?_#'MAZy\x0b-*#"
    assert f'{type(usage_entry_0.output_tokens).__module__}.{type(usage_entry_0.output_tokens).__qualname__}' == 'snippet_31.UsageAggregator'
    assert usage_entry_0.cache_creation_tokens == 0
    assert usage_entry_0.cache_read_tokens == 'xA;U\x0b*z'
    assert usage_entry_0.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert usage_entry_0.model == 'xA;U\x0b*z'
    assert usage_entry_0.message_id == "uN\\D?_#'MAZy\x0b-*#"
    assert usage_entry_0.request_id == ''
    assert module_1.UsageEntry.cache_creation_tokens == 0
    assert module_1.UsageEntry.cache_read_tokens == 0
    assert module_1.UsageEntry.cost_usd == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_1.UsageEntry.model == ''
    assert module_1.UsageEntry.message_id == ''
    assert module_1.UsageEntry.request_id == ''
    list_0 = [usage_entry_0, usage_entry_0, usage_entry_0]
    usage_aggregator_0.aggregate_daily(list_0, usage_entry_0, usage_entry_0)