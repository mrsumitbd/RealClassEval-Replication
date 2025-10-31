import pytest
import snippet_107 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    module_0.ColorMaps()

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = -5244
    color_maps_0 = module_0.ColorMaps(int_0)
    color_maps_0.list()

@pytest.mark.xfail(strict=True)
def test_case_2():
    int_0 = -5244
    color_maps_0 = module_0.ColorMaps(int_0)
    str_0 = 'eFnHrCS"ELoyT}*~Wn'
    dict_0 = {str_0: str_0}
    color_maps_0.register(dict_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    int_0 = -5226
    color_maps_0 = module_0.ColorMaps(int_0)
    str_0 = 'eFnH$C"ELoy:}*~Wn'
    dict_0 = {str_0: str_0}
    color_maps_0.register(dict_0, color_maps_0)