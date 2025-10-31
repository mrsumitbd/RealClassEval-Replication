import pytest
import snippet_237 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    float_0 = -1194.28
    none_type_0 = None
    list_0 = [float_0, float_0, float_0, float_0]
    str_0 = '%2USDK[0Rxun'
    multi_search_result_0 = module_0.MultiSearchResult(none_type_0, none_type_0, list_0, list_0, list_0, list_0, list_0, list_0, str_0)
    assert f'{type(multi_search_result_0).__module__}.{type(multi_search_result_0).__qualname__}' == 'snippet_237.MultiSearchResult'
    assert multi_search_result_0.id is None
    assert multi_search_result_0.content is None
    assert f'{type(multi_search_result_0.original_scores).__module__}.{type(multi_search_result_0.original_scores).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.original_scores) == 4
    assert f'{type(multi_search_result_0.source_uri).__module__}.{type(multi_search_result_0.source_uri).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.source_uri) == 4
    assert f'{type(multi_search_result_0.relative_path).__module__}.{type(multi_search_result_0.relative_path).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.relative_path) == 4
    assert f'{type(multi_search_result_0.language).__module__}.{type(multi_search_result_0.language).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.language) == 4
    assert f'{type(multi_search_result_0.authors).__module__}.{type(multi_search_result_0.authors).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.authors) == 4
    assert f'{type(multi_search_result_0.created_at).__module__}.{type(multi_search_result_0.created_at).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.created_at) == 4
    assert multi_search_result_0.summary == '%2USDK[0Rxun'
    assert f'{type(module_0.MultiSearchResult.to_jsonlines).__module__}.{type(module_0.MultiSearchResult.to_jsonlines).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.MultiSearchResult.to_string).__module__}.{type(module_0.MultiSearchResult.to_string).__qualname__}' == 'builtins.method'
    multi_search_result_0.__str__()

@pytest.mark.xfail(strict=True)
def test_case_1():
    float_0 = -1194.28
    none_type_0 = None
    list_0 = [float_0, float_0, float_0, float_0]
    str_0 = '%2USDK[0Rxun'
    multi_search_result_0 = module_0.MultiSearchResult(none_type_0, none_type_0, list_0, list_0, list_0, list_0, list_0, list_0, str_0)
    assert f'{type(multi_search_result_0).__module__}.{type(multi_search_result_0).__qualname__}' == 'snippet_237.MultiSearchResult'
    assert multi_search_result_0.id is None
    assert multi_search_result_0.content is None
    assert f'{type(multi_search_result_0.original_scores).__module__}.{type(multi_search_result_0.original_scores).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.original_scores) == 4
    assert f'{type(multi_search_result_0.source_uri).__module__}.{type(multi_search_result_0.source_uri).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.source_uri) == 4
    assert f'{type(multi_search_result_0.relative_path).__module__}.{type(multi_search_result_0.relative_path).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.relative_path) == 4
    assert f'{type(multi_search_result_0.language).__module__}.{type(multi_search_result_0.language).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.language) == 4
    assert f'{type(multi_search_result_0.authors).__module__}.{type(multi_search_result_0.authors).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.authors) == 4
    assert f'{type(multi_search_result_0.created_at).__module__}.{type(multi_search_result_0.created_at).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.created_at) == 4
    assert multi_search_result_0.summary == '%2USDK[0Rxun'
    assert f'{type(module_0.MultiSearchResult.to_jsonlines).__module__}.{type(module_0.MultiSearchResult.to_jsonlines).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.MultiSearchResult.to_string).__module__}.{type(module_0.MultiSearchResult.to_string).__qualname__}' == 'builtins.method'
    multi_search_result_0.calculate_relative_path(list_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    float_0 = -1194.28
    list_0 = [float_0, float_0, float_0, float_0]
    str_0 = '%2USDL[oRxYn'
    multi_search_result_0 = module_0.MultiSearchResult(float_0, float_0, list_0, list_0, list_0, list_0, list_0, list_0, str_0)
    assert f'{type(multi_search_result_0).__module__}.{type(multi_search_result_0).__qualname__}' == 'snippet_237.MultiSearchResult'
    assert multi_search_result_0.id == pytest.approx(-1194.28, abs=0.01, rel=0.01)
    assert multi_search_result_0.content == pytest.approx(-1194.28, abs=0.01, rel=0.01)
    assert f'{type(multi_search_result_0.original_scores).__module__}.{type(multi_search_result_0.original_scores).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.original_scores) == 4
    assert f'{type(multi_search_result_0.source_uri).__module__}.{type(multi_search_result_0.source_uri).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.source_uri) == 4
    assert f'{type(multi_search_result_0.relative_path).__module__}.{type(multi_search_result_0.relative_path).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.relative_path) == 4
    assert f'{type(multi_search_result_0.language).__module__}.{type(multi_search_result_0.language).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.language) == 4
    assert f'{type(multi_search_result_0.authors).__module__}.{type(multi_search_result_0.authors).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.authors) == 4
    assert f'{type(multi_search_result_0.created_at).__module__}.{type(multi_search_result_0.created_at).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.created_at) == 4
    assert multi_search_result_0.summary == '%2USDL[oRxYn'
    assert f'{type(module_0.MultiSearchResult.to_jsonlines).__module__}.{type(module_0.MultiSearchResult.to_jsonlines).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.MultiSearchResult.to_string).__module__}.{type(module_0.MultiSearchResult.to_string).__qualname__}' == 'builtins.method'
    multi_search_result_0.detect_language_from_extension(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    float_0 = -1194.28
    list_0 = [float_0, float_0, float_0, float_0]
    str_0 = 'd7f\nXG+twJ<JX oP'
    int_0 = -1190
    list_1 = []
    multi_search_result_0 = module_0.MultiSearchResult(list_0, str_0, list_0, int_0, list_0, str_0, list_1, list_0, str_0)
    assert f'{type(multi_search_result_0).__module__}.{type(multi_search_result_0).__qualname__}' == 'snippet_237.MultiSearchResult'
    assert f'{type(multi_search_result_0.id).__module__}.{type(multi_search_result_0.id).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.id) == 4
    assert multi_search_result_0.content == 'd7f\nXG+twJ<JX oP'
    assert f'{type(multi_search_result_0.original_scores).__module__}.{type(multi_search_result_0.original_scores).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.original_scores) == 4
    assert multi_search_result_0.source_uri == -1190
    assert f'{type(multi_search_result_0.relative_path).__module__}.{type(multi_search_result_0.relative_path).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.relative_path) == 4
    assert multi_search_result_0.language == 'd7f\nXG+twJ<JX oP'
    assert multi_search_result_0.authors == []
    assert f'{type(multi_search_result_0.created_at).__module__}.{type(multi_search_result_0.created_at).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.created_at) == 4
    assert multi_search_result_0.summary == 'd7f\nXG+twJ<JX oP'
    assert f'{type(module_0.MultiSearchResult.to_jsonlines).__module__}.{type(module_0.MultiSearchResult.to_jsonlines).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.MultiSearchResult.to_string).__module__}.{type(module_0.MultiSearchResult.to_string).__qualname__}' == 'builtins.method'
    str_1 = 'or8'
    str_2 = multi_search_result_0.calculate_relative_path(str_1, str_0)
    assert str_2 == 'or8'
    multi_search_result_0.to_json()

@pytest.mark.xfail(strict=True)
def test_case_4():
    float_0 = -1194.28
    none_type_0 = None
    list_0 = [float_0, float_0, float_0, float_0]
    str_0 = 'd7f\nXG+twJ<JX oP'
    int_0 = -1190
    list_1 = []
    multi_search_result_0 = module_0.MultiSearchResult(list_0, str_0, list_0, int_0, none_type_0, str_0, list_1, none_type_0, str_0)
    assert f'{type(multi_search_result_0).__module__}.{type(multi_search_result_0).__qualname__}' == 'snippet_237.MultiSearchResult'
    assert f'{type(multi_search_result_0.id).__module__}.{type(multi_search_result_0.id).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.id) == 4
    assert multi_search_result_0.content == 'd7f\nXG+twJ<JX oP'
    assert f'{type(multi_search_result_0.original_scores).__module__}.{type(multi_search_result_0.original_scores).__qualname__}' == 'builtins.list'
    assert len(multi_search_result_0.original_scores) == 4
    assert multi_search_result_0.source_uri == -1190
    assert multi_search_result_0.relative_path is None
    assert multi_search_result_0.language == 'd7f\nXG+twJ<JX oP'
    assert multi_search_result_0.authors == []
    assert multi_search_result_0.created_at is None
    assert multi_search_result_0.summary == 'd7f\nXG+twJ<JX oP'
    assert f'{type(module_0.MultiSearchResult.to_jsonlines).__module__}.{type(module_0.MultiSearchResult.to_jsonlines).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.MultiSearchResult.to_string).__module__}.{type(module_0.MultiSearchResult.to_string).__qualname__}' == 'builtins.method'
    str_1 = 'or8'
    str_2 = multi_search_result_0.calculate_relative_path(str_1, str_0)
    assert str_2 == 'or8'
    str_3 = multi_search_result_0.to_json()
    assert str_3 == '{"id":[-1194.28,-1194.28,-1194.28,-1194.28],"source":-1190,"path":null,"lang":"d7f\\nxg+twj<jx op","created":"","author":"","score":[-1194.28,-1194.28,-1194.28,-1194.28],"code":"d7f\\nXG+twJ<JX oP","summary":"d7f\\nXG+twJ<JX oP"}'
    multi_search_result_0.__str__()