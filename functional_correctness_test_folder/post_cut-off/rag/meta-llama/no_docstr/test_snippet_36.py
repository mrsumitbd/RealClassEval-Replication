import snippet_36 as module_0
import rich.console as module_1

def test_case_0():
    loading_screen_component_0 = module_0.LoadingScreenComponent()
    assert f'{type(loading_screen_component_0).__module__}.{type(loading_screen_component_0).__qualname__}' == 'snippet_36.LoadingScreenComponent'
    loading_screen_component_0.create_loading_screen()
    str_0 = 'N`jRxt5W?k .>M\x0cNi\\'
    var_0 = loading_screen_component_0.create_loading_screen_renderable(custom_message=str_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'rich.console.Group'
    assert var_0.fit is True
    assert f'{type(module_1.Group.renderables).__module__}.{type(module_1.Group.renderables).__qualname__}' == 'builtins.property'

def test_case_1():
    loading_screen_component_0 = module_0.LoadingScreenComponent()
    assert f'{type(loading_screen_component_0).__module__}.{type(loading_screen_component_0).__qualname__}' == 'snippet_36.LoadingScreenComponent'
    str_0 = '#EHHnJN(!A\tz9~og8'
    var_0 = loading_screen_component_0.create_loading_screen_renderable(str_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'rich.console.Group'
    assert var_0.fit is True
    assert f'{type(module_1.Group.renderables).__module__}.{type(module_1.Group.renderables).__qualname__}' == 'builtins.property'