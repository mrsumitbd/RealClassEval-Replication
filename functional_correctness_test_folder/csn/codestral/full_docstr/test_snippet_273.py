import pytest
import snippet_273 as module_0

def test_case_0():
    int_0 = 1613
    base_pagination_0 = module_0.BasePagination()
    assert f'{type(base_pagination_0).__module__}.{type(base_pagination_0).__qualname__}' == 'snippet_273.BasePagination'
    with pytest.raises(NotImplementedError):
        base_pagination_0.paginate_query(int_0, int_0)

def test_case_1():
    complex_0 = -668 - 976j
    base_pagination_0 = module_0.BasePagination()
    assert f'{type(base_pagination_0).__module__}.{type(base_pagination_0).__qualname__}' == 'snippet_273.BasePagination'
    with pytest.raises(NotImplementedError):
        base_pagination_0.get_paginated_response(complex_0)