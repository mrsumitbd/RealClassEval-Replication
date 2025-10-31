import snippet_131 as module_0

def test_case_0():
    null_func_0 = module_0.NullFunc()
    null_func_0.__call__()

def test_case_1():
    null_func_0 = module_0.NullFunc()
    none_type_0 = None
    list_0 = [none_type_0, none_type_0]
    null_func_0.__call__(*list_0)

def test_case_2():
    null_func_0 = module_0.NullFunc()
    null_func_0.distance(null_func_0)
    none_type_0 = None
    list_0 = [none_type_0, none_type_0]
    null_func_0.__call__(*list_0)

def test_case_3():
    module_0.NullFunc()

def test_case_4():
    null_func_0 = module_0.NullFunc()
    none_type_0 = None
    null_func_0.distance(none_type_0)
    null_func_0.__call__()