import snippet_133 as module_0

def test_case_0():
    none_type_0 = None
    dependencies_configuration_0 = module_0.DependenciesConfiguration(none_type_0)
    assert f'{type(dependencies_configuration_0).__module__}.{type(dependencies_configuration_0).__qualname__}' == 'snippet_133.DependenciesConfiguration'
    assert dependencies_configuration_0.tool_dependency_dir is None
    assert dependencies_configuration_0.dependency_resolvers_config_file is None
    assert dependencies_configuration_0.use_tool_dependencies is False
    assert module_0.TYPE_CHECKING is False