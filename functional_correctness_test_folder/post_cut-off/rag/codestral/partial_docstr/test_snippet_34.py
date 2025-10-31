import snippet_34 as module_0
import rich.theme as module_1

def test_case_0():
    adaptive_color_scheme_0 = module_0.AdaptiveColorScheme()
    assert f'{type(adaptive_color_scheme_0).__module__}.{type(adaptive_color_scheme_0).__qualname__}' == 'snippet_34.AdaptiveColorScheme'
    theme_0 = adaptive_color_scheme_0.get_light_background_theme()
    assert f'{type(theme_0).__module__}.{type(theme_0).__qualname__}' == 'rich.theme.Theme'
    assert f'{type(theme_0.styles).__module__}.{type(theme_0.styles).__qualname__}' == 'builtins.dict'
    assert len(theme_0.styles) == 189
    assert f'{type(module_1.Theme.config).__module__}.{type(module_1.Theme.config).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Theme.from_file).__module__}.{type(module_1.Theme.from_file).__qualname__}' == 'builtins.method'
    assert f'{type(module_1.Theme.read).__module__}.{type(module_1.Theme.read).__qualname__}' == 'builtins.method'

def test_case_1():
    dict_0 = {}
    adaptive_color_scheme_0 = module_0.AdaptiveColorScheme(**dict_0)
    assert f'{type(adaptive_color_scheme_0).__module__}.{type(adaptive_color_scheme_0).__qualname__}' == 'snippet_34.AdaptiveColorScheme'
    theme_0 = adaptive_color_scheme_0.get_dark_background_theme()
    assert f'{type(theme_0).__module__}.{type(theme_0).__qualname__}' == 'rich.theme.Theme'
    assert f'{type(theme_0.styles).__module__}.{type(theme_0.styles).__qualname__}' == 'builtins.dict'
    assert len(theme_0.styles) == 189
    assert f'{type(module_1.Theme.config).__module__}.{type(module_1.Theme.config).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Theme.from_file).__module__}.{type(module_1.Theme.from_file).__qualname__}' == 'builtins.method'
    assert f'{type(module_1.Theme.read).__module__}.{type(module_1.Theme.read).__qualname__}' == 'builtins.method'

def test_case_2():
    adaptive_color_scheme_0 = module_0.AdaptiveColorScheme()
    assert f'{type(adaptive_color_scheme_0).__module__}.{type(adaptive_color_scheme_0).__qualname__}' == 'snippet_34.AdaptiveColorScheme'
    theme_0 = adaptive_color_scheme_0.get_classic_theme()
    assert f'{type(theme_0).__module__}.{type(theme_0).__qualname__}' == 'rich.theme.Theme'
    assert f'{type(theme_0.styles).__module__}.{type(theme_0.styles).__qualname__}' == 'builtins.dict'
    assert len(theme_0.styles) == 188
    assert f'{type(module_1.Theme.config).__module__}.{type(module_1.Theme.config).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Theme.from_file).__module__}.{type(module_1.Theme.from_file).__qualname__}' == 'builtins.method'
    assert f'{type(module_1.Theme.read).__module__}.{type(module_1.Theme.read).__qualname__}' == 'builtins.method'
    theme_1 = adaptive_color_scheme_0.get_dark_background_theme()
    assert f'{type(theme_1).__module__}.{type(theme_1).__qualname__}' == 'rich.theme.Theme'
    assert f'{type(theme_1.styles).__module__}.{type(theme_1.styles).__qualname__}' == 'builtins.dict'
    assert len(theme_1.styles) == 189
    assert f'{type(module_1.DEFAULT_STYLES).__module__}.{type(module_1.DEFAULT_STYLES).__qualname__}' == 'builtins.dict'
    assert len(module_1.DEFAULT_STYLES) == 151