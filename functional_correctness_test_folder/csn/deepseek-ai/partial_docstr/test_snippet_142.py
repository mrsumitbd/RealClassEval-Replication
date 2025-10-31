import snippet_142 as module_0

def test_case_0():
    float_0 = 1081.5533
    project_template_0 = module_0.ProjectTemplate()
    assert f'{type(project_template_0).__module__}.{type(project_template_0).__qualname__}' == 'snippet_142.ProjectTemplate'
    project_template_0.get_project_template(build_dir=float_0)