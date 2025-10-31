import pytest
import snippet_204 as module_0
import pipask._vendor.pip._internal.exceptions as module_1

def test_case_0():
    str_0 = 'v;QwTiwhpM5O11]Ei~=('
    with pytest.raises(module_1.InvalidWheelFilename):
        module_0.Wheel(str_0)