import pytest
import snippet_59 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    none_type_1 = None
    error_summary_0 = module_0._ErrorSummary(none_type_1, none_type_1, none_type_1)
    assert f'{type(error_summary_0).__module__}.{type(error_summary_0).__qualname__}' == 'snippet_59._ErrorSummary'
    assert error_summary_0.origin is None
    assert error_summary_0.example_message is None
    assert error_summary_0.failed_indexed_executions is None
    assert f'{type(module_0._ErrorSummary.num_failed).__module__}.{type(module_0._ErrorSummary.num_failed).__qualname__}' == 'builtins.property'
    error_summary_0.add_execution(error_summary_0, none_type_0)