import pytest
import snippet_103 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '@3d\x0benxzEh+0*w/u\x0b|'
    str_1 = 'Sk1DXG'
    str_2 = '>9P^wgeNdZ6fu'
    triton_remote_model_0 = module_0.TritonRemoteModel(str_0, str_1, str_2)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    module_0.TritonRemoteModel(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    str_0 = '?sNz$N\x0b]l'
    module_0.TritonRemoteModel(none_type_0, scheme=str_0)