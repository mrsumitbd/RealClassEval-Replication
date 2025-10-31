import pytest
import snippet_45 as module_0

def test_case_0():
    bool_0 = True
    token_store_base_0 = module_0.TokenStoreBase(bool_0)
    assert f'{type(token_store_base_0).__module__}.{type(token_store_base_0).__qualname__}' == 'snippet_45.TokenStoreBase'
    assert token_store_base_0.token_collection is True

def test_case_1():
    bool_0 = True
    token_store_base_0 = module_0.TokenStoreBase()
    assert f'{type(token_store_base_0).__module__}.{type(token_store_base_0).__qualname__}' == 'snippet_45.TokenStoreBase'
    assert token_store_base_0.token_collection == 'default'
    with pytest.raises(NotImplementedError):
        token_store_base_0.save_token_pair(bool_0, bool_0, bool_0)

def test_case_2():
    token_store_base_0 = module_0.TokenStoreBase()
    assert f'{type(token_store_base_0).__module__}.{type(token_store_base_0).__qualname__}' == 'snippet_45.TokenStoreBase'
    assert token_store_base_0.token_collection == 'default'
    with pytest.raises(NotImplementedError):
        token_store_base_0.load_token_pair(token_store_base_0, token_store_base_0)

def test_case_3():
    none_type_0 = None
    token_store_base_0 = module_0.TokenStoreBase()
    assert f'{type(token_store_base_0).__module__}.{type(token_store_base_0).__qualname__}' == 'snippet_45.TokenStoreBase'
    assert token_store_base_0.token_collection == 'default'
    with pytest.raises(NotImplementedError):
        token_store_base_0.has_token(token_store_base_0, none_type_0)