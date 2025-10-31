import pytest
import snippet_149 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '/\x0c1OJaP\x0c`V'
    module_0.ArticleEvaluator(str_0)

def test_case_1():
    module_0.ArticleEvaluator()