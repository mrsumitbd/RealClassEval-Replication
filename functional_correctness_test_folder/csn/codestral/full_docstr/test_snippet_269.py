import snippet_269 as module_0

def test_case_0():
    task_config_0 = module_0._TaskConfig()
    assert f'{type(task_config_0).__module__}.{type(task_config_0).__qualname__}' == 'snippet_269._TaskConfig'
    assert f'{type(module_0._TaskConfig.KW_ARGS_ERROR_REGEX).__module__}.{type(module_0._TaskConfig.KW_ARGS_ERROR_REGEX).__qualname__}' == 're.Pattern'
    assert f'{type(module_0._TaskConfig.from_dict).__module__}.{type(module_0._TaskConfig.from_dict).__qualname__}' == 'builtins.method'
    task_config_0.to_dict()