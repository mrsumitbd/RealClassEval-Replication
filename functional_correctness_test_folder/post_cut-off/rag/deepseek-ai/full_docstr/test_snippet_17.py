import pytest
import snippet_17 as module_0

def test_case_0():
    base_embedding_0 = module_0.BaseEmbedding()
    assert f'{type(base_embedding_0).__module__}.{type(base_embedding_0).__qualname__}' == 'snippet_17.BaseEmbedding'
    assert f'{type(module_0.BaseEmbedding.dimension).__module__}.{type(module_0.BaseEmbedding.dimension).__qualname__}' == 'builtins.property'
    str_0 = 'g6iD7kX\r'
    list_0 = [str_0, str_0]
    base_embedding_0.embed_documents(list_0)

def test_case_1():
    tuple_0 = ()
    base_embedding_0 = module_0.BaseEmbedding()
    assert f'{type(base_embedding_0).__module__}.{type(base_embedding_0).__qualname__}' == 'snippet_17.BaseEmbedding'
    assert f'{type(module_0.BaseEmbedding.dimension).__module__}.{type(module_0.BaseEmbedding.dimension).__qualname__}' == 'builtins.property'
    base_embedding_0.embed_chunks(tuple_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '^P&@s-)26hRiJ '
    base_embedding_0 = module_0.BaseEmbedding()
    assert f'{type(base_embedding_0).__module__}.{type(base_embedding_0).__qualname__}' == 'snippet_17.BaseEmbedding'
    assert f'{type(module_0.BaseEmbedding.dimension).__module__}.{type(module_0.BaseEmbedding.dimension).__qualname__}' == 'builtins.property'
    base_embedding_0.embed_query(base_embedding_0)
    bool_0 = False
    base_embedding_0.embed_chunks(str_0, bool_0)