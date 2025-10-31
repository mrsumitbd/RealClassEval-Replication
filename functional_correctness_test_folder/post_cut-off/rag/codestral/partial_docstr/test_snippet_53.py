import pytest
import snippet_53 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    affine_transform2_d_0.solve(affine_transform2_d_0)

def test_case_1():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    affine_transform2_d_0.is_solution(affine_transform2_d_0, affine_transform2_d_0)

def test_case_2():
    module_0.AffineTransform2D()

@pytest.mark.xfail(strict=True)
def test_case_3():
    affine_transform2_d_0 = module_0.AffineTransform2D()
    dict_0 = {affine_transform2_d_0: affine_transform2_d_0, affine_transform2_d_0: affine_transform2_d_0, affine_transform2_d_0: affine_transform2_d_0}
    affine_transform2_d_0.is_solution(dict_0, dict_0)
    affine_transform2_d_0.solve(affine_transform2_d_0)