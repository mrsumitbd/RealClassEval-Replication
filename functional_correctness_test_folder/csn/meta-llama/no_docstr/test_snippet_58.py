import pytest
import snippet_58 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    morphological_struct_factory_0 = module_0.MorphologicalStructFactory()
    bool_0 = True
    morphological_struct_factory_0.get_disk(bool_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    morphological_struct_factory_0 = module_0.MorphologicalStructFactory()
    int_0 = -1958
    int_1 = -2107
    morphological_struct_factory_0.get_rectangle(int_0, int_1)

@pytest.mark.xfail(strict=True)
def test_case_2():
    morphological_struct_factory_0 = module_0.MorphologicalStructFactory()
    morphological_struct_factory_0.get_square(morphological_struct_factory_0)

def test_case_3():
    module_0.MorphologicalStructFactory()