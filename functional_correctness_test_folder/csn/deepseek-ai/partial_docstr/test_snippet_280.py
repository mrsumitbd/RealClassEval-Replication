import snippet_280 as module_0

def test_case_0():
    str_0 = "Oo'.@Ha&uMmc,;~W\rudy"
    system_field_context_0 = module_0.SystemFieldContext(str_0, str_0)
    assert f'{type(system_field_context_0).__module__}.{type(system_field_context_0).__qualname__}' == 'snippet_280.SystemFieldContext'
    assert f'{type(module_0.SystemFieldContext.field).__module__}.{type(module_0.SystemFieldContext.field).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.SystemFieldContext.record_cls).__module__}.{type(module_0.SystemFieldContext.record_cls).__qualname__}' == 'builtins.property'