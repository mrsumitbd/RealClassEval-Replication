import pytest
import snippet_106 as module_0

def test_case_0():
    chroma_embedding_function_0 = module_0.ChromaEmbeddingFunction()
    assert f'{type(chroma_embedding_function_0).__module__}.{type(chroma_embedding_function_0).__qualname__}' == 'snippet_106.ChromaEmbeddingFunction'
    assert module_0.TYPE_CHECKING is False
    with pytest.raises(ValueError):
        chroma_embedding_function_0.__call__(chroma_embedding_function_0)

def test_case_1():
    dict_0 = {}
    chroma_embedding_function_0 = module_0.ChromaEmbeddingFunction(**dict_0)
    assert f'{type(chroma_embedding_function_0).__module__}.{type(chroma_embedding_function_0).__qualname__}' == 'snippet_106.ChromaEmbeddingFunction'
    assert module_0.TYPE_CHECKING is False
    with pytest.raises(ValueError):
        module_0.ChromaEmbeddingFunction(chroma_embedding_function_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    chroma_embedding_function_0 = module_0.ChromaEmbeddingFunction()
    assert f'{type(chroma_embedding_function_0).__module__}.{type(chroma_embedding_function_0).__qualname__}' == 'snippet_106.ChromaEmbeddingFunction'
    assert module_0.TYPE_CHECKING is False
    str_0 = ''
    chroma_embedding_function_0.__call__(str_0)

def test_case_3():
    chroma_embedding_function_0 = module_0.ChromaEmbeddingFunction()
    assert f'{type(chroma_embedding_function_0).__module__}.{type(chroma_embedding_function_0).__qualname__}' == 'snippet_106.ChromaEmbeddingFunction'
    assert module_0.TYPE_CHECKING is False
    str_0 = chroma_embedding_function_0.name()
    assert str_0 == 'minishlab/potion-retrieval-32M'
    with pytest.raises(ValueError):
        chroma_embedding_function_0.__call__(chroma_embedding_function_0)