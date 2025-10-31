import snippet_295 as module_0
import collections as module_1

def test_case_0():
    str_0 = 'pL0JGu#'
    str_1 = 'J3.f#]NOFY9p+g|v\x0b*&'
    dict_0 = {str_0: str_0, str_1: str_1}
    list_0 = [dict_0, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{'pL0JGu#': 'pL0JGu#', 'J3.f#]NOFY9p+g|v\x0b*&': 'J3.f#]NOFY9p+g|v\x0b*&'}, {'pL0JGu#': 'pL0JGu#', 'J3.f#]NOFY9p+g|v\x0b*&': 'J3.f#]NOFY9p+g|v\x0b*&'}, {'pL0JGu#': 'pL0JGu#', 'J3.f#]NOFY9p+g|v\x0b*&': 'J3.f#]NOFY9p+g|v\x0b*&'}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1

def test_case_1():
    str_0 = ';c'
    str_1 = 'HR'
    list_0 = []
    dict_0 = {str_1: list_0}
    list_1 = [dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{'HR': []}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    tool_selector_0.select_tools(str_0)

def test_case_2():
    list_0 = []
    tool_selector_0 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == []
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 0
    tool_selector_0.select_by_names(list_0)
    str_0 = ''
    bool_0 = True
    tool_selector_0.select_tools(str_0, overlap=bool_0)

def test_case_3():
    dict_0 = {}
    list_0 = [dict_0]
    tool_selector_0 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    str_0 = 'B]r&%_cx=b}4!1x '
    list_1 = [str_0, str_0]
    tool_selector_0.select_by_names(list_1)
    tool_selector_0.filter_by_keywords(list_1)

def test_case_4():
    str_0 = '+"n?&9#'
    str_1 = '\\zgEChhwQ>r4Ep1z-'
    list_0 = [str_0, str_1]
    str_2 = "%a#w-I'Y3etQP?&T0j;\x0c"
    dict_0 = {str_0: list_0, str_2: list_0, str_2: list_0}
    str_3 = ']'
    dict_1 = {str_3: str_3}
    list_1 = [dict_1]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{']': ']'}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    tool_selector_0.filter_by_roles(dict_0)

def test_case_5():
    dict_0 = {}
    tool_selector_0 = module_0.ToolSelector(dict_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == {}
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 0
    tool_selector_0.filter_by_roles(dict_0)
    list_0 = [dict_0]
    tool_selector_1 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_1).__module__}.{type(tool_selector_1).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_1.tools == [{}]
    assert f'{type(tool_selector_1.tools_by_category).__module__}.{type(tool_selector_1.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_1.tools_by_category) == 1

def test_case_6():
    dict_0 = {}
    list_0 = [dict_0]
    tool_selector_0 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    str_0 = 'B]r&%_cx=b}4!1x '
    list_1 = [str_0, str_0]
    tool_selector_0.filter_by_keywords(list_1)

def test_case_7():
    str_0 = '^\r+\ty& 2iop?boA\te'
    str_1 = ''
    dict_0 = {str_1: str_1}
    list_0 = [dict_0]
    tool_selector_0 = module_0.ToolSelector(list_0)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{'': ''}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    int_0 = 603
    tool_selector_0.select_tools(str_0, int_0)

def test_case_8():
    none_type_0 = None

def test_case_9():
    str_0 = '^\r+y&Y0)2iop?boA\te'
    list_0 = [str_0, str_0]
    dict_0 = {str_0: str_0, str_0: str_0}
    dict_1 = {}
    list_1 = [dict_0, dict_1, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{'^\r+y&Y0)2iop?boA\te': '^\r+y&Y0)2iop?boA\te'}, {}, {'^\r+y&Y0)2iop?boA\te': '^\r+y&Y0)2iop?boA\te'}, {'^\r+y&Y0)2iop?boA\te': '^\r+y&Y0)2iop?boA\te'}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    tool_selector_0.select_by_names(str_0)
    str_1 = 'l@CB\r\r|*\rF^\x0c.nz'
    tool_selector_0.filter_by_roles(dict_0)
    bool_0 = False
    tool_selector_0.filter_by_keywords(list_0, bool_0)
    str_2 = ''
    dict_2 = {str_2: str_2}
    list_2 = [dict_2]
    dict_3 = tool_selector_0.filter_by_roles(dict_2)
    tool_selector_1 = module_0.ToolSelector(list_2)
    assert f'{type(tool_selector_1).__module__}.{type(tool_selector_1).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_1.tools == [{'': ''}]
    assert f'{type(tool_selector_1.tools_by_category).__module__}.{type(tool_selector_1.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_1.tools_by_category) == 1
    tool_selector_1.select_tools(str_1)
    tool_selector_1.filter_by_keywords(dict_3)

def test_case_10():
    bool_0 = True
    str_0 = '.fJ\nG]y-RNJ6*'
    str_1 = "sa$Vl'x|\tc%Y"
    dict_0 = {str_1: str_1, str_1: str_1, str_1: str_1, str_1: str_1}
    dict_1 = {str_1: dict_0}
    str_2 = '\x0cw\t}T\n}r*4p'
    str_3 = 'k!:\x0cmc\\2I_%'
    list_0 = [str_0, str_2, str_3]
    list_1 = [dict_1, dict_1, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    tool_selector_0.filter_by_keywords(list_0)
    tool_selector_1 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_1).__module__}.{type(tool_selector_1).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_1.tools == [{"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}]
    assert f'{type(tool_selector_1.tools_by_category).__module__}.{type(tool_selector_1.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_1.tools_by_category) == 1
    tool_selector_1.select_tools(str_0, bool_0)

def test_case_11():
    str_0 = '^\r+\ty& 2iopboA\te'
    list_0 = [str_0, str_0]
    dict_0 = {str_0: list_0, str_0: str_0, str_0: str_0, str_0: str_0}
    defaultdict_0 = module_1.defaultdict()
    assert f'{type(defaultdict_0).__module__}.{type(defaultdict_0).__qualname__}' == 'collections.defaultdict'
    assert len(defaultdict_0) == 0
    assert f'{type(module_1.defaultdict.default_factory).__module__}.{type(module_1.defaultdict.default_factory).__qualname__}' == 'builtins.member_descriptor'
    list_1 = [dict_0, defaultdict_0, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert f'{type(tool_selector_0.tools).__module__}.{type(tool_selector_0.tools).__qualname__}' == 'builtins.list'
    assert len(tool_selector_0.tools) == 4
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    str_1 = 'l@CB\r\r|*\rF^\x0c.nz'
    tool_selector_0.select_by_names(str_1)
    str_2 = ''
    dict_1 = {str_2: str_2}
    list_2 = [dict_1]
    tool_selector_1 = module_0.ToolSelector(list_2)
    assert f'{type(tool_selector_1).__module__}.{type(tool_selector_1).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_1.tools == [{'': ''}]
    assert f'{type(tool_selector_1.tools_by_category).__module__}.{type(tool_selector_1.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_1.tools_by_category) == 1
    str_3 = 'p\\ yBzmbzK{i0SoDil72'
    var_0 = tool_selector_1.select_tools(str_3, overlap=dict_0)
    tool_selector_1.filter_by_keywords(list_0, var_0)

def test_case_12():
    str_0 = '#)D\'kY"~'
    bool_0 = True
    str_1 = '.fJ\nG]y-RNJ6*'
    str_2 = "sa$Vl'x|\tc%Y"
    dict_0 = {str_2: str_2, str_2: str_2, str_2: str_2, str_2: str_2}
    dict_1 = {str_2: dict_0}
    str_3 = '\x0cw\t}T\n}r*4p'
    str_4 = 'k!:\x0cmc\\2I_%'
    list_0 = [str_1, str_3, str_4]
    list_1 = [dict_1, dict_1, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    list_2 = tool_selector_0.filter_by_keywords(list_0)
    tool_selector_0.filter_by_keywords(list_2, bool_0)
    tool_selector_1 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_1).__module__}.{type(tool_selector_1).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_1.tools == [{"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}, {"sa$Vl'x|\tc%Y": "sa$Vl'x|\tc%Y"}]
    assert f'{type(tool_selector_1.tools_by_category).__module__}.{type(tool_selector_1.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_1.tools_by_category) == 1
    bool_1 = True
    tool_selector_1.select_tools(str_0, bool_1)

def test_case_13():
    str_0 = '^\r+\ty& 2iop?boA\te'
    list_0 = [str_0, str_0]
    dict_0 = {}
    list_1 = [dict_0, dict_0, dict_0, dict_0]
    tool_selector_0 = module_0.ToolSelector(list_1)
    assert f'{type(tool_selector_0).__module__}.{type(tool_selector_0).__qualname__}' == 'snippet_295.ToolSelector'
    assert tool_selector_0.tools == [{}, {}, {}, {}]
    assert f'{type(tool_selector_0.tools_by_category).__module__}.{type(tool_selector_0.tools_by_category).__qualname__}' == 'collections.defaultdict'
    assert len(tool_selector_0.tools_by_category) == 1
    tool_selector_0.select_by_names(list_0)
    str_1 = ''
    dict_1 = {str_1: str_1}
    tool_selector_0.filter_by_roles(dict_1)
    var_0 = module_1.defaultdict()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'collections.defaultdict'
    assert len(var_0) == 0
    assert f'{type(module_1.defaultdict.default_factory).__module__}.{type(module_1.defaultdict.default_factory).__qualname__}' == 'builtins.member_descriptor'
    int_0 = 602
    tool_selector_0.select_tools(var_0, int_0)