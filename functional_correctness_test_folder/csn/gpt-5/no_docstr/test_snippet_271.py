import pytest
import platform as module_0
import snippet_271 as module_1

def test_case_0():
    none_type_0 = None

@pytest.mark.xfail(strict=True)
def test_case_1():
    set_0 = module_0.release()
    module_1.Subplot(set_0, set_0, title_font_size=set_0, state_text_buffer=set_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    set_0 = set()
    module_1.Subplot(set_0, set_0, title_font_size=set_0, state_text_buffer=set_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    var_0 = module_0.python_revision()
    var_1 = var_0.rsplit()
    module_1.Subplot(var_1, var_1, state_names=var_1, state_font_size=var_0, label_side=var_1)