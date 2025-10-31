import pytest
import snippet_308 as module_0
import uuid as module_1

def test_case_0():
    str_0 = 'v\tg'
    in_memory_blob_store_0 = module_0.InMemoryBlobStore()
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 100
    assert in_memory_blob_store_0.access_order == []
    with pytest.raises(FileNotFoundError):
        in_memory_blob_store_0.load(str_0)

def test_case_1():
    in_memory_blob_store_0 = module_0.InMemoryBlobStore()
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 100
    assert in_memory_blob_store_0.access_order == []
    with pytest.raises(FileNotFoundError):
        in_memory_blob_store_0.info(in_memory_blob_store_0)

def test_case_2():
    in_memory_blob_store_0 = module_0.InMemoryBlobStore()
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 100
    assert in_memory_blob_store_0.access_order == []
    str_0 = 'u6.vH?s;4P/%\x0b/U{'
    in_memory_blob_store_0.delete(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    var_0 = module_1.getnode()
    assert var_0 == 190070690681122
    assert module_1.RESERVED_NCS == 'reserved for NCS compatibility'
    assert module_1.RFC_4122 == 'specified in RFC 4122'
    assert module_1.RESERVED_MICROSOFT == 'reserved for Microsoft compatibility'
    assert module_1.RESERVED_FUTURE == 'reserved for future definition'
    assert f'{type(module_1.NAMESPACE_DNS).__module__}.{type(module_1.NAMESPACE_DNS).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_URL).__module__}.{type(module_1.NAMESPACE_URL).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_OID).__module__}.{type(module_1.NAMESPACE_OID).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_X500).__module__}.{type(module_1.NAMESPACE_X500).__qualname__}' == 'uuid.UUID'
    in_memory_blob_store_0 = module_0.InMemoryBlobStore(var_0)
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 190070690681122
    assert in_memory_blob_store_0.access_order == []
    in_memory_blob_store_0.save(var_0, var_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    var_0 = module_1.uuid4()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'uuid.UUID'
    assert module_1.RESERVED_NCS == 'reserved for NCS compatibility'
    assert module_1.RFC_4122 == 'specified in RFC 4122'
    assert module_1.RESERVED_MICROSOFT == 'reserved for Microsoft compatibility'
    assert module_1.RESERVED_FUTURE == 'reserved for future definition'
    assert f'{type(module_1.NAMESPACE_DNS).__module__}.{type(module_1.NAMESPACE_DNS).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_URL).__module__}.{type(module_1.NAMESPACE_URL).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_OID).__module__}.{type(module_1.NAMESPACE_OID).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.NAMESPACE_X500).__module__}.{type(module_1.NAMESPACE_X500).__qualname__}' == 'uuid.UUID'
    assert f'{type(module_1.UUID.bytes).__module__}.{type(module_1.UUID.bytes).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.bytes_le).__module__}.{type(module_1.UUID.bytes_le).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.fields).__module__}.{type(module_1.UUID.fields).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.time_low).__module__}.{type(module_1.UUID.time_low).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.time_mid).__module__}.{type(module_1.UUID.time_mid).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.time_hi_version).__module__}.{type(module_1.UUID.time_hi_version).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.clock_seq_hi_variant).__module__}.{type(module_1.UUID.clock_seq_hi_variant).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.clock_seq_low).__module__}.{type(module_1.UUID.clock_seq_low).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.time).__module__}.{type(module_1.UUID.time).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.clock_seq).__module__}.{type(module_1.UUID.clock_seq).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.node).__module__}.{type(module_1.UUID.node).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.hex).__module__}.{type(module_1.UUID.hex).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.urn).__module__}.{type(module_1.UUID.urn).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.variant).__module__}.{type(module_1.UUID.variant).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.version).__module__}.{type(module_1.UUID.version).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.UUID.int).__module__}.{type(module_1.UUID.int).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.UUID.is_safe).__module__}.{type(module_1.UUID.is_safe).__qualname__}' == 'builtins.member_descriptor'
    in_memory_blob_store_0 = module_0.InMemoryBlobStore(var_0)
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert f'{type(in_memory_blob_store_0.max_size).__module__}.{type(in_memory_blob_store_0.max_size).__qualname__}' == 'uuid.UUID'
    assert in_memory_blob_store_0.access_order == []
    in_memory_blob_store_0.save(var_0, var_0)

def test_case_5():
    int_0 = 4119
    in_memory_blob_store_0 = module_0.InMemoryBlobStore(int_0)
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 4119
    assert in_memory_blob_store_0.access_order == []
    str_0 = "k'-a^\n5{\t>9nRK-pS"
    str_1 = 'MB'
    dict_0 = {str_0: str_1, str_1: int_0}
    str_2 = in_memory_blob_store_0.save(str_0, dict_0)
    assert f'{type(in_memory_blob_store_0.metadata).__module__}.{type(in_memory_blob_store_0.metadata).__qualname__}' == 'builtins.dict'
    assert len(in_memory_blob_store_0.metadata) == 1
    in_memory_blob_store_0.info(str_2)
    str_3 = 'IWf;)'
    in_memory_blob_store_0.delete(str_3)
    str_4 = '6v:&Mg!8}g<wr1j'
    with pytest.raises(FileNotFoundError):
        in_memory_blob_store_0.load(str_4)

def test_case_6():
    int_0 = 4119
    str_0 = "k'-a^\n5{\t>9nRK-pS"
    in_memory_blob_store_0 = module_0.InMemoryBlobStore()
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 100
    assert in_memory_blob_store_0.access_order == []
    dict_0 = {str_0: str_0, str_0: int_0}
    str_1 = in_memory_blob_store_0.save(str_0, dict_0)
    assert f'{type(in_memory_blob_store_0.metadata).__module__}.{type(in_memory_blob_store_0.metadata).__qualname__}' == 'builtins.dict'
    assert len(in_memory_blob_store_0.metadata) == 1
    bytes_0 = in_memory_blob_store_0.load(str_1)
    assert bytes_0 == "k'-a^\n5{\t>9nRK-pS"
    str_2 = 'Sa\\+4u:JVEAsf>"=d'
    with pytest.raises(FileNotFoundError):
        in_memory_blob_store_0.load(str_2)

def test_case_7():
    int_0 = 4119
    str_0 = 'MB'
    in_memory_blob_store_0 = module_0.InMemoryBlobStore()
    assert f'{type(in_memory_blob_store_0).__module__}.{type(in_memory_blob_store_0).__qualname__}' == 'snippet_308.InMemoryBlobStore'
    assert in_memory_blob_store_0.blobs == {}
    assert in_memory_blob_store_0.metadata == {}
    assert in_memory_blob_store_0.max_size == 100
    assert in_memory_blob_store_0.access_order == []
    dict_0 = {str_0: str_0, str_0: int_0}
    str_1 = in_memory_blob_store_0.save(str_0, dict_0)
    assert f'{type(in_memory_blob_store_0.metadata).__module__}.{type(in_memory_blob_store_0.metadata).__qualname__}' == 'builtins.dict'
    assert len(in_memory_blob_store_0.metadata) == 1
    bytes_0 = in_memory_blob_store_0.load(str_1)
    assert bytes_0 == 'MB'