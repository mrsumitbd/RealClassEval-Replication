import pytest
import snippet_252 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    r_g_b888_format_0 = module_0.RGB888Format()
    assert f'{type(r_g_b888_format_0).__module__}.{type(r_g_b888_format_0).__qualname__}' == 'snippet_252.RGB888Format'
    r_g_b888_format_0.get_pixel(r_g_b888_format_0, r_g_b888_format_0, r_g_b888_format_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    r_g_b888_format_0 = module_0.RGB888Format()
    assert f'{type(r_g_b888_format_0).__module__}.{type(r_g_b888_format_0).__qualname__}' == 'snippet_252.RGB888Format'
    r_g_b888_format_0.fill_rect(bool_0, bool_0, bool_0, bool_0, bool_0, bool_0)

def test_case_2():
    bool_0 = False
    r_g_b888_format_0 = module_0.RGB888Format()
    assert f'{type(r_g_b888_format_0).__module__}.{type(r_g_b888_format_0).__qualname__}' == 'snippet_252.RGB888Format'
    r_g_b888_format_0.fill_rect(bool_0, bool_0, bool_0, bool_0, bool_0, bool_0)

def test_case_3():
    bool_0 = True
    r_g_b888_format_0 = module_0.RGB888Format()
    assert f'{type(r_g_b888_format_0).__module__}.{type(r_g_b888_format_0).__qualname__}' == 'snippet_252.RGB888Format'
    bool_1 = True
    bool_2 = False
    r_g_b888_format_0.fill_rect(bool_0, bool_1, bool_1, bool_0, bool_2, bool_2)