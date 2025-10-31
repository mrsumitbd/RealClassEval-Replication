import snippet_253 as module_0

def test_case_0():
    str_0 = 'E8 0I=~U1%k)\t/6'
    prompt_logger_0 = module_0.PromptLogger(str_0)
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'E8 0I=~U1%k)\t/6'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'

def test_case_1():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'

def test_case_2():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    list_0 = prompt_logger_0.get_recent_logs()
    prompt_logger_0.log_prompt(list_0)
    str_0 = 'Ap]ef\t7dxU'
    str_1 = "M7^(mk3\x0c>\r'1w<M+U\\"
    prompt_logger_0.log_formatted_prompt(str_0, prompt_logger_0, str_1)

def test_case_3():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    dict_0 = {}
    list_0 = [dict_0]
    prompt_logger_0.log_prompt(list_0, prompt_logger_0)
    prompt_logger_0.clear_logs()

def test_case_4():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    prompt_logger_0.log_prompt(prompt_logger_0)

def test_case_5():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    none_type_0 = None
    prompt_logger_0.log_formatted_prompt(none_type_0, none_type_0, character_name=none_type_0)

def test_case_6():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    prompt_logger_0.get_recent_logs()

def test_case_7():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    str_0 = 'y)(R3z%C{4L<rp\tk:'
    prompt_logger_0.get_recent_logs(str_0)

def test_case_8():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    prompt_logger_0.clear_logs()

def test_case_9():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    list_0 = prompt_logger_0.get_recent_logs(prompt_logger_0)
    str_0 = '1\x0b+'
    prompt_logger_0.log_formatted_prompt(prompt_logger_0, str_0, list_0)
    var_0 = prompt_logger_0.clear_logs()
    str_1 = 'G1R(\tiN)'
    prompt_logger_0.log_formatted_prompt(str_1, var_0)

def test_case_10():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    str_0 = 'y)(R3z%C{4L<rp\tk:'
    prompt_logger_0.get_recent_logs(str_0)

def test_case_11():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    str_0 = 'y)(R3z%C{4L<rp\tk:'
    var_0 = prompt_logger_0.log_prompt(str_0)
    prompt_logger_1 = module_0.PromptLogger(str_0)
    assert f'{type(prompt_logger_1).__module__}.{type(prompt_logger_1).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_1.log_file == 'y)(R3z%C{4L<rp\tk:'
    assert f'{type(prompt_logger_1.logger).__module__}.{type(prompt_logger_1.logger).__qualname__}' == 'logging.Logger'
    str_1 = 'S@b"kP,'
    prompt_logger_1.get_recent_logs()
    prompt_logger_0.log_formatted_prompt(str_0, str_1, character_name=var_0, user_query=prompt_logger_1)

def test_case_12():
    prompt_logger_0 = module_0.PromptLogger()
    assert f'{type(prompt_logger_0).__module__}.{type(prompt_logger_0).__qualname__}' == 'snippet_253.PromptLogger'
    assert prompt_logger_0.log_file == 'log.txt'
    assert f'{type(prompt_logger_0.logger).__module__}.{type(prompt_logger_0.logger).__qualname__}' == 'logging.Logger'
    int_0 = -1748
    prompt_logger_0.get_recent_logs(int_0)