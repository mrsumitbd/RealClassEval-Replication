import snippet_113 as module_0

def test_case_0():
    none_type_0 = None
    file_like_i_o_0 = module_0.FileLikeIO()
    assert f'{type(file_like_i_o_0).__module__}.{type(file_like_i_o_0).__qualname__}' == 'snippet_113.FileLikeIO'
    file_like_i_o_0.remove(none_type_0)
    file_like_i_o_1 = module_0.FileLikeIO()
    assert f'{type(file_like_i_o_1).__module__}.{type(file_like_i_o_1).__qualname__}' == 'snippet_113.FileLikeIO'
    file_like_i_o_1.open(file_like_i_o_1)

def test_case_1():
    bool_0 = False
    file_like_i_o_0 = module_0.FileLikeIO()
    assert f'{type(file_like_i_o_0).__module__}.{type(file_like_i_o_0).__qualname__}' == 'snippet_113.FileLikeIO'
    file_like_i_o_0.remove(bool_0)
    file_like_i_o_1 = module_0.FileLikeIO()
    assert f'{type(file_like_i_o_1).__module__}.{type(file_like_i_o_1).__qualname__}' == 'snippet_113.FileLikeIO'
    file_like_i_o_1.exists(bool_0)