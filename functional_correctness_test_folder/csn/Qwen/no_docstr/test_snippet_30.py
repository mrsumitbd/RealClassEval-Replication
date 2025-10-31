import snippet_30 as module_0

def test_case_0():
    int_0 = 891
    lazy_op_result_0 = module_0.LazyOpResult(int_0, int_0, int_0)
    assert f'{type(lazy_op_result_0).__module__}.{type(lazy_op_result_0).__qualname__}' == 'snippet_30.LazyOpResult'
    assert lazy_op_result_0.expr == 891
    assert lazy_op_result_0.weld_type == 891
    assert lazy_op_result_0.dim == 891