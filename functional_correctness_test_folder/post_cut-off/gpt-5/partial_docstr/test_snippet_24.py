import snippet_24 as module_0

def test_case_0():
    local_path_extractor_0 = module_0.LocalPathExtractor()
    assert f'{type(local_path_extractor_0).__module__}.{type(local_path_extractor_0).__qualname__}' == 'snippet_24.LocalPathExtractor'
    str_0 = 'VIUP6o^Ygo3f97.4a m'
    local_path_extractor_0.extract_local_paths(str_0)

def test_case_1():
    local_path_extractor_0 = module_0.LocalPathExtractor()
    assert f'{type(local_path_extractor_0).__module__}.{type(local_path_extractor_0).__qualname__}' == 'snippet_24.LocalPathExtractor'
    str_0 = "tqlFHixd'k Sig\t"
    bool_0 = local_path_extractor_0.is_local_path(str_0)
    assert bool_0 is False

def test_case_2():
    local_path_extractor_0 = module_0.LocalPathExtractor()
    assert f'{type(local_path_extractor_0).__module__}.{type(local_path_extractor_0).__qualname__}' == 'snippet_24.LocalPathExtractor'
    str_0 = 'p~\\\'k\'(4~"'
    local_path_extractor_0.extract_local_paths(str_0)

def test_case_3():
    local_path_extractor_0 = module_0.LocalPathExtractor()
    assert f'{type(local_path_extractor_0).__module__}.{type(local_path_extractor_0).__qualname__}' == 'snippet_24.LocalPathExtractor'
    str_0 = 'kZzr%3 DTlykU[J-97z'
    local_path_extractor_0.extract_local_paths(str_0)
    bool_0 = local_path_extractor_0.is_local_path(str_0)
    assert bool_0 is False
    str_1 = '.'
    bool_1 = local_path_extractor_0.is_local_path(str_1)
    assert bool_1 is True