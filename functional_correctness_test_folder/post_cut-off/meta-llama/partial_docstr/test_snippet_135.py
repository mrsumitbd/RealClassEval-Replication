import pytest
import snippet_135 as module_0

def test_case_0():
    none_type_0 = None
    g_p_u_manager_0 = module_0.GPUManager(none_type_0)
    with pytest.raises(ValueError):
        g_p_u_manager_0.get_memory_usage()

def test_case_1():
    bool_0 = False