import snippet_262 as module_0

def test_case_0():
    s_t_messages_0 = module_0.STMessages()
    s_t_messages_0.warning()
    s_t_messages_0.success()
    s_t_messages_0.error()

def test_case_1():
    s_t_messages_0 = module_0.STMessages()
    str_0 = '"|bp<\t*\ni^y&uUf:\'R'
    s_t_messages_0.error(str_0)
    str_1 = 'xMZQLeJ=\n4'
    s_t_messages_0.warning(str_1)

def test_case_2():
    dict_0 = {}
    s_t_messages_0 = module_0.STMessages(**dict_0)
    s_t_messages_0.skull()

def test_case_3():
    complex_0 = -331.5 - 2947.522112j