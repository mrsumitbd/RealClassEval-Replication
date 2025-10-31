import pytest
import snippet_81 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = '~!O:G-#'
    module_0.YOLOv8TFLite(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '~!O:G-#'
    module_0.YOLOv8TFLite(str_0, metadata=str_0)