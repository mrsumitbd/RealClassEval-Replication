import pytest
import snippet_86 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    letter_box_0 = module_0.LetterBox()
    none_type_0 = None
    letter_box_0.__call__(none_type_0, none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    letter_box_0 = module_0.LetterBox()
    letter_box_0.__call__(letter_box_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    letter_box_0 = module_0.LetterBox(scaleFill=none_type_0)
    letter_box_0.__call__(none_type_0, letter_box_0)

def test_case_3():
    module_0.LetterBox()