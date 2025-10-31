import snippet_346 as module_0

def test_case_0():
    dict_0 = {}
    event_data_normalizer_0 = module_0.EventDataNormalizer()
    assert f'{type(event_data_normalizer_0).__module__}.{type(event_data_normalizer_0).__qualname__}' == 'snippet_346.EventDataNormalizer'
    event_data_normalizer_0.normalize_event_data(dict_0, dict_0)

def test_case_1():
    dict_0 = {}
    event_data_normalizer_0 = module_0.EventDataNormalizer()
    assert f'{type(event_data_normalizer_0).__module__}.{type(event_data_normalizer_0).__qualname__}' == 'snippet_346.EventDataNormalizer'
    event_data_normalizer_0.extract_user_id(dict_0)

def test_case_2():
    str_0 = 'G@Zr4U'
    dict_0 = {str_0: str_0}
    event_data_normalizer_0 = module_0.EventDataNormalizer()
    assert f'{type(event_data_normalizer_0).__module__}.{type(event_data_normalizer_0).__qualname__}' == 'snippet_346.EventDataNormalizer'
    event_data_normalizer_0.extract_target_info(dict_0)