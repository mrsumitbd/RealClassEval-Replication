import pytest
import snippet_186 as module_0

def test_case_0():
    unified_auth_factory_0 = module_0.UnifiedAuthFactory()
    str_0 = 'u9xet~rTDZ#n)\x0c!Jn#w'
    with pytest.raises(ValueError):
        unified_auth_factory_0.create_model_auth(str_0)

def test_case_1():
    unified_auth_factory_0 = module_0.UnifiedAuthFactory()
    with pytest.raises(ValueError):
        unified_auth_factory_0.create_storage_auth(unified_auth_factory_0)

def test_case_2():
    module_0.UnifiedAuthFactory()