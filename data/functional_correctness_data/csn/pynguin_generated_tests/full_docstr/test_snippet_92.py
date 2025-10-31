import snippet_92 as module_0

def test_case_0():
    int_0 = 2997
    none_type_0 = None
    pipeline_definition_0 = module_0.PipelineDefinition(int_0, none_type_0)
    assert f'{type(pipeline_definition_0).__module__}.{type(pipeline_definition_0).__qualname__}' == 'snippet_92.PipelineDefinition'
    assert f'{type(module_0.PipelineDefinition.info).__module__}.{type(module_0.PipelineDefinition.info).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.PipelineDefinition.pipeline).__module__}.{type(module_0.PipelineDefinition.pipeline).__qualname__}' == 'builtins.member_descriptor'
    none_type_1 = None
    pipeline_definition_1 = module_0.PipelineDefinition(none_type_1, none_type_1)
    assert f'{type(pipeline_definition_1).__module__}.{type(pipeline_definition_1).__qualname__}' == 'snippet_92.PipelineDefinition'
    var_0 = pipeline_definition_1.__eq__(pipeline_definition_0)
    assert var_0 is False
    none_type_2 = None
    bytes_0 = b'+\xe0y\xdc\xa5\xa0\xbd'
    pipeline_definition_2 = module_0.PipelineDefinition(bytes_0, bytes_0)
    assert f'{type(pipeline_definition_2).__module__}.{type(pipeline_definition_2).__qualname__}' == 'snippet_92.PipelineDefinition'
    pipeline_definition_3 = module_0.PipelineDefinition(none_type_2, pipeline_definition_2)
    assert f'{type(pipeline_definition_3).__module__}.{type(pipeline_definition_3).__qualname__}' == 'snippet_92.PipelineDefinition'
    var_1 = pipeline_definition_3.__eq__(none_type_2)
    assert var_1 is False

def test_case_1():
    none_type_0 = None
    bool_0 = False
    pipeline_definition_0 = module_0.PipelineDefinition(bool_0, bool_0)
    assert f'{type(pipeline_definition_0).__module__}.{type(pipeline_definition_0).__qualname__}' == 'snippet_92.PipelineDefinition'
    assert f'{type(module_0.PipelineDefinition.info).__module__}.{type(module_0.PipelineDefinition.info).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.PipelineDefinition.pipeline).__module__}.{type(module_0.PipelineDefinition.pipeline).__qualname__}' == 'builtins.member_descriptor'
    var_0 = pipeline_definition_0.__eq__(none_type_0)
    assert var_0 is False

def test_case_2():
    none_type_0 = None
    pipeline_definition_0 = module_0.PipelineDefinition(none_type_0, none_type_0)
    assert f'{type(pipeline_definition_0).__module__}.{type(pipeline_definition_0).__qualname__}' == 'snippet_92.PipelineDefinition'
    assert f'{type(module_0.PipelineDefinition.info).__module__}.{type(module_0.PipelineDefinition.info).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.PipelineDefinition.pipeline).__module__}.{type(module_0.PipelineDefinition.pipeline).__qualname__}' == 'builtins.member_descriptor'
    pipeline_definition_1 = module_0.PipelineDefinition(none_type_0, pipeline_definition_0)
    assert f'{type(pipeline_definition_1).__module__}.{type(pipeline_definition_1).__qualname__}' == 'snippet_92.PipelineDefinition'
    var_0 = pipeline_definition_1.__eq__(none_type_0)
    assert var_0 is False
    var_1 = pipeline_definition_0.__eq__(pipeline_definition_0)
    assert var_1 is True

def test_case_3():
    str_0 = '"('
    pipeline_definition_0 = module_0.PipelineDefinition(str_0, str_0)
    assert f'{type(pipeline_definition_0).__module__}.{type(pipeline_definition_0).__qualname__}' == 'snippet_92.PipelineDefinition'
    assert f'{type(module_0.PipelineDefinition.info).__module__}.{type(module_0.PipelineDefinition.info).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.PipelineDefinition.pipeline).__module__}.{type(module_0.PipelineDefinition.pipeline).__qualname__}' == 'builtins.member_descriptor'