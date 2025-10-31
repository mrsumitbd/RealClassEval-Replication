import builtins as module_0
import snippet_93 as module_1

def test_case_0():
    object_0 = module_0.object()
    list_0 = [object_0, object_0]
    pipeline_info_0 = module_1.PipelineInfo(list_0, list_0, object_0, is_loader_cascading=object_0)
    assert f'{type(pipeline_info_0).__module__}.{type(pipeline_info_0).__qualname__}' == 'snippet_93.PipelineInfo'
    assert f'{type(module_1.PipelineInfo.is_loader_cascading).__module__}.{type(module_1.PipelineInfo.is_loader_cascading).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.is_parent_cascading).__module__}.{type(module_1.PipelineInfo.is_parent_cascading).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.loader).__module__}.{type(module_1.PipelineInfo.loader).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.parent).__module__}.{type(module_1.PipelineInfo.parent).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.pipeline_name).__module__}.{type(module_1.PipelineInfo.pipeline_name).__qualname__}' == 'builtins.member_descriptor'
    var_0 = pipeline_info_0.__eq__(pipeline_info_0)
    assert var_0 is True

def test_case_1():
    bool_0 = True
    pipeline_info_0 = module_1.PipelineInfo(bool_0, bool_0, bool_0)
    assert f'{type(pipeline_info_0).__module__}.{type(pipeline_info_0).__qualname__}' == 'snippet_93.PipelineInfo'
    assert f'{type(module_1.PipelineInfo.is_loader_cascading).__module__}.{type(module_1.PipelineInfo.is_loader_cascading).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.is_parent_cascading).__module__}.{type(module_1.PipelineInfo.is_parent_cascading).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.loader).__module__}.{type(module_1.PipelineInfo.loader).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.parent).__module__}.{type(module_1.PipelineInfo.parent).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.PipelineInfo.pipeline_name).__module__}.{type(module_1.PipelineInfo.pipeline_name).__qualname__}' == 'builtins.member_descriptor'
    var_0 = pipeline_info_0.__eq__(bool_0)
    assert var_0 is False