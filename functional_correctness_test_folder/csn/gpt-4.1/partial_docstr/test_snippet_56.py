import snippet_56 as module_0

def test_case_0():
    collection_0 = module_0.Collection()
    assert f'{type(collection_0).__module__}.{type(collection_0).__qualname__}' == 'snippet_56.Collection'
    collection_0.__len__()

def test_case_1():
    int_0 = -155
    list_0 = []
    collection_0 = module_0.Collection(*list_0)
    assert f'{type(collection_0).__module__}.{type(collection_0).__qualname__}' == 'snippet_56.Collection'
    collection_0.__delitem__(int_0)

def test_case_2():
    str_0 = '(`\n'
    collection_0 = module_0.Collection()
    assert f'{type(collection_0).__module__}.{type(collection_0).__qualname__}' == 'snippet_56.Collection'
    collection_0.__contains__(str_0)