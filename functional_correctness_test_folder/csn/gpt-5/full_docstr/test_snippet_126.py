import pytest
import snippet_126 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'ywq(o\ttk[PTNmcY'
    module_0.LowestCommonAncestorRMQ(str_0)

def test_case_1():
    str_0 = 'ad~iVo'
    tuple_0 = ()
    list_0 = [tuple_0, str_0]
    lowest_common_ancestor_r_m_q_0 = module_0.LowestCommonAncestorRMQ(list_0)
    assert f'{type(lowest_common_ancestor_r_m_q_0).__module__}.{type(lowest_common_ancestor_r_m_q_0).__qualname__}' == 'snippet_126.LowestCommonAncestorRMQ'
    assert lowest_common_ancestor_r_m_q_0.last == [0, None]
    assert f'{type(lowest_common_ancestor_r_m_q_0.rmq).__module__}.{type(lowest_common_ancestor_r_m_q_0.rmq).__qualname__}' == 'tryalgo.range_minimum_query.RangeMinQuery'