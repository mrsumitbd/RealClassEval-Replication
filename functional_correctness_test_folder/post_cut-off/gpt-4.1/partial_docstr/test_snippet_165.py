import snippet_165 as module_0

def test_case_0():
    tool_history_0 = module_0.ToolHistory()
    assert f'{type(tool_history_0).__module__}.{type(tool_history_0).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_0.get_visited_urls()

def test_case_1():
    str_0 = 'u0?<Kb<A-|:^!0'
    str_1 = 'Fh=^f.P_`4I*'
    list_0 = [str_0, str_1, str_0]
    tool_history_0 = module_0.ToolHistory()
    assert f'{type(tool_history_0).__module__}.{type(tool_history_0).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_0.add_visited_urls(list_0)

def test_case_2():
    str_0 = 'Tcw7b3XU8Cc=}i7J~Cz'
    str_1 = 'f9H_\t#b\nW_+E'
    list_0 = [str_0, str_1, str_0]
    tool_history_0 = module_0.ToolHistory()
    assert f'{type(tool_history_0).__module__}.{type(tool_history_0).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_0.add_searched_queries(list_0)

def test_case_3():
    str_0 = 'q(\r^Nh'
    str_1 = "SwPmx~95E_nI'ta{'?"
    list_0 = [str_0, str_1]
    tool_history_0 = module_0.ToolHistory()
    assert f'{type(tool_history_0).__module__}.{type(tool_history_0).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_0.add_visited_urls(list_0)
    tool_history_1 = module_0.ToolHistory()
    assert f'{type(tool_history_1).__module__}.{type(tool_history_1).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_1.get_visited_urls()
    tool_history_2 = module_0.ToolHistory()
    assert f'{type(tool_history_2).__module__}.{type(tool_history_2).__qualname__}' == 'snippet_165.ToolHistory'
    tool_history_2.get_searched_queries()