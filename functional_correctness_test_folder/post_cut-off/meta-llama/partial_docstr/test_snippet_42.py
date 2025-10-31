import pytest
import snippet_42 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    screen_manager_0 = module_0.ScreenManager()
    assert f'{type(screen_manager_0).__module__}.{type(screen_manager_0).__qualname__}' == 'snippet_42.ScreenManager'
    assert screen_manager_0.screen_width == 80
    assert screen_manager_0.screen_height == 24
    assert screen_manager_0.margin_left == 0
    assert screen_manager_0.margin_right == 0
    assert screen_manager_0.margin_top == 0
    assert screen_manager_0.margin_bottom == 0
    assert module_0.ScreenManager.DEFAULT_SCREEN_WIDTH == 80
    assert module_0.ScreenManager.DEFAULT_SCREEN_HEIGHT == 24
    assert module_0.ScreenManager.DEFAULT_MARGIN == 0
    none_type_0 = screen_manager_0.set_screen_dimensions(bool_0, bool_0)
    assert screen_manager_0.screen_width is False
    assert screen_manager_0.screen_height is False
    none_type_1 = None
    complex_0 = 265 - 1050.46j
    list_0 = [none_type_1, complex_0, screen_manager_0]
    screen_manager_0.create_full_screen_layout(list_0)

def test_case_1():
    screen_manager_0 = module_0.ScreenManager()
    assert f'{type(screen_manager_0).__module__}.{type(screen_manager_0).__qualname__}' == 'snippet_42.ScreenManager'
    assert screen_manager_0.screen_width == 80
    assert screen_manager_0.screen_height == 24
    assert screen_manager_0.margin_left == 0
    assert screen_manager_0.margin_right == 0
    assert screen_manager_0.margin_top == 0
    assert screen_manager_0.margin_bottom == 0
    assert module_0.ScreenManager.DEFAULT_SCREEN_WIDTH == 80
    assert module_0.ScreenManager.DEFAULT_SCREEN_HEIGHT == 24
    assert module_0.ScreenManager.DEFAULT_MARGIN == 0
    str_0 = '1(xop,nZV.9hzl`'
    screen_manager_0.create_full_screen_layout(str_0)
    none_type_0 = screen_manager_0.set_screen_dimensions(screen_manager_0, screen_manager_0)
    assert f'{type(screen_manager_0.screen_width).__module__}.{type(screen_manager_0.screen_width).__qualname__}' == 'snippet_42.ScreenManager'
    assert f'{type(screen_manager_0.screen_height).__module__}.{type(screen_manager_0.screen_height).__qualname__}' == 'snippet_42.ScreenManager'

def test_case_2():
    screen_manager_0 = module_0.ScreenManager()
    assert f'{type(screen_manager_0).__module__}.{type(screen_manager_0).__qualname__}' == 'snippet_42.ScreenManager'
    assert screen_manager_0.screen_width == 80
    assert screen_manager_0.screen_height == 24
    assert screen_manager_0.margin_left == 0
    assert screen_manager_0.margin_right == 0
    assert screen_manager_0.margin_top == 0
    assert screen_manager_0.margin_bottom == 0
    assert module_0.ScreenManager.DEFAULT_SCREEN_WIDTH == 80
    assert module_0.ScreenManager.DEFAULT_SCREEN_HEIGHT == 24
    assert module_0.ScreenManager.DEFAULT_MARGIN == 0
    screen_manager_0.set_margins()

def test_case_3():
    int_0 = 717
    screen_manager_0 = module_0.ScreenManager()
    assert f'{type(screen_manager_0).__module__}.{type(screen_manager_0).__qualname__}' == 'snippet_42.ScreenManager'
    assert screen_manager_0.screen_width == 80
    assert screen_manager_0.screen_height == 24
    assert screen_manager_0.margin_left == 0
    assert screen_manager_0.margin_right == 0
    assert screen_manager_0.margin_top == 0
    assert screen_manager_0.margin_bottom == 0
    assert module_0.ScreenManager.DEFAULT_SCREEN_WIDTH == 80
    assert module_0.ScreenManager.DEFAULT_SCREEN_HEIGHT == 24
    assert module_0.ScreenManager.DEFAULT_MARGIN == 0
    none_type_0 = screen_manager_0.set_screen_dimensions(int_0, int_0)
    assert screen_manager_0.screen_width == 717
    assert screen_manager_0.screen_height == 717