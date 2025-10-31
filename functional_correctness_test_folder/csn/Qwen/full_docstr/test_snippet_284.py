import pytest
import snippet_284 as module_0
import rasterio.enums as module_1

def test_case_0():
    none_type_0 = None
    r_i_o_dataset_0 = module_0.RIODataset(none_type_0, none_type_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile is None
    assert r_i_o_dataset_0.overviews is None
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize == 256

@pytest.mark.xfail(strict=True)
def test_case_1():
    set_0 = set()
    module_0.RIODataset(set_0, overviews_resampling=set_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    list_0 = []
    r_i_o_dataset_0 = module_0.RIODataset(list_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile == []
    assert r_i_o_dataset_0.overviews is None
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize == 256
    r_i_o_dataset_0.__setitem__(list_0, r_i_o_dataset_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = '3J!^!:ZQ&>f\n(i'
    r_i_o_dataset_0 = module_0.RIODataset(str_0, str_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile == '3J!^!:ZQ&>f\n(i'
    assert r_i_o_dataset_0.overviews == '3J!^!:ZQ&>f\n(i'
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize == 256
    r_i_o_dataset_0.close()

@pytest.mark.xfail(strict=True)
def test_case_4():
    none_type_0 = None
    r_i_o_dataset_0 = module_0.RIODataset(none_type_0, overviews_minsize=none_type_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile is None
    assert r_i_o_dataset_0.overviews is None
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize is None
    r_i_o_dataset_0.close()

@pytest.mark.xfail(strict=True)
def test_case_5():
    dict_0 = {}
    r_i_o_dataset_0 = module_0.RIODataset(dict_0, dict_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile == {}
    assert r_i_o_dataset_0.overviews == {}
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize == 256
    r_i_o_dataset_0.close()

@pytest.mark.xfail(strict=True)
def test_case_6():
    none_type_0 = None
    r_i_o_dataset_0 = module_0.RIODataset(none_type_0, overviews_minsize=none_type_0)
    assert f'{type(r_i_o_dataset_0).__module__}.{type(r_i_o_dataset_0).__qualname__}' == 'snippet_284.RIODataset'
    assert r_i_o_dataset_0.rfile is None
    assert r_i_o_dataset_0.overviews is None
    assert r_i_o_dataset_0.overviews_resampling == module_1.Resampling.nearest
    assert r_i_o_dataset_0.overviews_minsize is None
    list_0 = [none_type_0, none_type_0, none_type_0]
    r_i_o_dataset_0.__setitem__(list_0, r_i_o_dataset_0)