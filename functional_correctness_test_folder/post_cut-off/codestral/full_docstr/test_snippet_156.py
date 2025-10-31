import dataclasses as module_0
import snippet_156 as module_1

def test_case_0():
    int_0 = -1322
    int_1 = 107
    none_type_0 = None
    bool_0 = False
    none_type_1 = None
    var_0 = module_0.dataclass(init=int_0, repr=bool_0, eq=int_0, match_args=none_type_1, kw_only=int_0, slots=none_type_1)
    assert f'{type(module_0.MISSING).__module__}.{type(module_0.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_0.KW_ONLY).__module__}.{type(module_0.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    var_1 = var_0.__eq__(none_type_0)
    diff_hunk_0 = module_1.DiffHunk(int_1, int_1, none_type_1, none_type_1, var_1)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start == 107
    assert diff_hunk_0.old_count == 107
    assert diff_hunk_0.new_start is None
    assert diff_hunk_0.new_count is None
    assert f'{type(diff_hunk_0.lines).__module__}.{type(diff_hunk_0.lines).__qualname__}' == 'builtins.NotImplementedType'
    diff_hunk_0.get_new_line_number(int_0)

def test_case_1():
    bool_0 = False
    int_0 = -2186
    none_type_0 = None
    str_0 = 'K_|)'
    list_0 = [str_0, str_0]
    diff_hunk_0 = module_1.DiffHunk(bool_0, bool_0, int_0, none_type_0, list_0)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start is False
    assert diff_hunk_0.old_count is False
    assert diff_hunk_0.new_start == -2186
    assert diff_hunk_0.new_count is None
    assert diff_hunk_0.lines == ['K_|)', 'K_|)']
    var_0 = diff_hunk_0.get_new_line_number(bool_0)
    assert var_0 == -2186

def test_case_2():
    none_type_0 = None
    bool_0 = False
    str_0 = 'LFaPH5M~$'
    list_0 = [str_0]
    diff_hunk_0 = module_1.DiffHunk(bool_0, bool_0, bool_0, bool_0, list_0)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start is False
    assert diff_hunk_0.old_count is False
    assert diff_hunk_0.new_start is False
    assert diff_hunk_0.new_count is False
    assert diff_hunk_0.lines == ['LFaPH5M~$']
    diff_hunk_0.contains_line_change(none_type_0)

def test_case_3():
    bool_0 = True
    bool_1 = False
    int_0 = -2186
    none_type_0 = None
    str_0 = 'K_|)'
    list_0 = [str_0, str_0]
    diff_hunk_0 = module_1.DiffHunk(bool_1, bool_1, int_0, none_type_0, list_0)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start is False
    assert diff_hunk_0.old_count is False
    assert diff_hunk_0.new_start == -2186
    assert diff_hunk_0.new_count is None
    assert diff_hunk_0.lines == ['K_|)', 'K_|)']
    var_0 = diff_hunk_0.get_new_line_number(bool_0)
    assert var_0 == -2185

def test_case_4():
    int_0 = 1071
    list_0 = []
    diff_hunk_0 = module_1.DiffHunk(int_0, int_0, int_0, int_0, list_0)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start == 1071
    assert diff_hunk_0.old_count == 1071
    assert diff_hunk_0.new_start == 1071
    assert diff_hunk_0.new_count == 1071
    assert diff_hunk_0.lines == []
    diff_hunk_0.get_new_line_number(int_0)

def test_case_5():
    none_type_0 = None
    bytes_0 = b'\x9c\x8a'
    bool_0 = True
    int_0 = -213
    diff_hunk_0 = module_1.DiffHunk(int_0, bytes_0, int_0, none_type_0, none_type_0)
    assert f'{type(diff_hunk_0).__module__}.{type(diff_hunk_0).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_0.old_start == -213
    assert diff_hunk_0.old_count == b'\x9c\x8a'
    assert diff_hunk_0.new_start == -213
    assert diff_hunk_0.new_count is None
    assert diff_hunk_0.lines is None
    int_1 = -3609
    list_0 = diff_hunk_0.__repr__()
    assert list_0 == "DiffHunk(old_start=-213, old_count=b'\\x9c\\x8a', new_start=-213, new_count=None, lines=None)"
    diff_hunk_1 = module_1.DiffHunk(bool_0, int_1, int_1, bool_0, list_0)
    assert f'{type(diff_hunk_1).__module__}.{type(diff_hunk_1).__qualname__}' == 'snippet_156.DiffHunk'
    assert diff_hunk_1.old_start is True
    assert diff_hunk_1.old_count == -3609
    assert diff_hunk_1.new_start == -3609
    assert diff_hunk_1.new_count is True
    assert diff_hunk_1.lines == "DiffHunk(old_start=-213, old_count=b'\\x9c\\x8a', new_start=-213, new_count=None, lines=None)"
    var_0 = diff_hunk_1.get_new_line_number(bool_0)
    assert var_0 == -3608
    str_0 = "'>.{|GuN"
    diff_hunk_1.contains_line_change(str_0)