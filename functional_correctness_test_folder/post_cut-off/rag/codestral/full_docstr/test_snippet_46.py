import pytest
import snippet_46 as module_0
import urllib.request as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    affine_transform2_d_0.solve(affine_transform2_d_0)

def test_case_1():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    affine_transform2_d_0.is_solution(affine_transform2_d_0, affine_transform2_d_0)

def test_case_2():
    module_0.AffineTransform2D()

def test_case_3():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    affine_transform2_d_0.is_solution(affine_transform2_d_0, affine_transform2_d_0)
    var_0 = module_1.thishost()
    assert module_1.MAXFTPCACHE == 10
    assert module_1.ftpcache == {}
    affine_transform2_d_0.is_solution(var_0, affine_transform2_d_0)