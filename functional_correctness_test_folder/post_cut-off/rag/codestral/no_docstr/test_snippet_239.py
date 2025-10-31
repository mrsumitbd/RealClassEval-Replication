import snippet_239 as module_0

def test_case_0():
    str_0 = "1t#Ji'N"
    tag_0 = module_0.Tag(str_0, updatedAt=str_0)
    assert f'{type(tag_0).__module__}.{type(tag_0).__qualname__}' == 'snippet_239.Tag'
    assert tag_0.name == "1t#Ji'N"
    assert tag_0.id is None
    assert tag_0.createdAt is None
    assert tag_0.updatedAt == "1t#Ji'N"
    assert module_0.Tag.id is None
    assert module_0.Tag.createdAt is None
    assert module_0.Tag.updatedAt is None
    assert f'{type(module_0.Tag.from_dict).__module__}.{type(module_0.Tag.from_dict).__qualname__}' == 'builtins.method'
    tag_0.to_dict()

def test_case_1():
    str_0 = "1t#Ji'Nlv"
    tag_0 = module_0.Tag(str_0, str_0)
    assert f'{type(tag_0).__module__}.{type(tag_0).__qualname__}' == 'snippet_239.Tag'
    assert tag_0.name == "1t#Ji'Nlv"
    assert tag_0.id == "1t#Ji'Nlv"
    assert tag_0.createdAt is None
    assert tag_0.updatedAt is None
    assert module_0.Tag.id is None
    assert module_0.Tag.createdAt is None
    assert module_0.Tag.updatedAt is None
    assert f'{type(module_0.Tag.from_dict).__module__}.{type(module_0.Tag.from_dict).__qualname__}' == 'builtins.method'
    tag_0.to_dict()