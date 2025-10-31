import pytest
import snippet_288 as module_0

def test_case_0():
    str_0 = 'z%iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'z%iqFr,#]>;`Or'
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'eiVpcUZyLCNdPjtgT3I='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None

def test_case_1():
    parser_extension_config_0 = module_0.ParserExtensionConfig()
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log is None
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None

def test_case_2():
    parser_extension_config_0 = module_0.ParserExtensionConfig()
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log is None
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    with pytest.raises(ValueError):
        parser_extension_config_0.validate()

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'z2iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig()
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log is None
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    module_0.ParserExtensionConfig(field_extractors=str_0, dynamic_parsing=str_0)

def test_case_4():
    str_0 = 'z2iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    parser_extension_config_1 = module_0.ParserExtensionConfig(str_0, str_0)
    assert f'{type(parser_extension_config_1).__module__}.{type(parser_extension_config_1).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_1.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_1.parser_config == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_1.field_extractors is None
    assert parser_extension_config_1.dynamic_parsing is None
    assert parser_extension_config_1.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert parser_extension_config_1.encoded_cbn_snippet == 'ejJpcUZyLCNdPjtgT3I='
    parser_extension_config_2 = module_0.ParserExtensionConfig(dynamic_parsing=parser_extension_config_0)
    assert f'{type(parser_extension_config_2).__module__}.{type(parser_extension_config_2).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_2.log is None
    assert parser_extension_config_2.parser_config is None
    assert parser_extension_config_2.field_extractors is None
    assert f'{type(parser_extension_config_2.dynamic_parsing).__module__}.{type(parser_extension_config_2.dynamic_parsing).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    parser_extension_config_3 = module_0.ParserExtensionConfig(str_0, field_extractors=parser_extension_config_2)
    assert f'{type(parser_extension_config_3).__module__}.{type(parser_extension_config_3).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_3.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_3.parser_config is None
    assert f'{type(parser_extension_config_3.field_extractors).__module__}.{type(parser_extension_config_3.field_extractors).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_3.dynamic_parsing is None
    assert parser_extension_config_3.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    none_type_0 = None
    with pytest.raises(ValueError):
        parser_extension_config_1.encode_base64(none_type_0)

def test_case_5():
    str_0 = 'W!o.wMYYak4$6><"XqS'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0, str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'W!o.wMYYak4$6><"XqS'
    assert parser_extension_config_0.parser_config == 'W!o.wMYYak4$6><"XqS'
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'VyFvLndNWVlhazQkNj48IlhxUw=='
    assert parser_extension_config_0.encoded_cbn_snippet == 'VyFvLndNWVlhazQkNj48IlhxUw=='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None

@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = 'z2iqFr,#]>;`Or'
    module_0.ParserExtensionConfig(dynamic_parsing=str_0)

def test_case_7():
    str_0 = 'z2iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0, str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_0.parser_config == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert parser_extension_config_0.encoded_cbn_snippet == 'ejJpcUZyLCNdPjtgT3I='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    parser_extension_config_1 = module_0.ParserExtensionConfig(dynamic_parsing=parser_extension_config_0)
    assert f'{type(parser_extension_config_1).__module__}.{type(parser_extension_config_1).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_1.log is None
    assert parser_extension_config_1.parser_config is None
    assert parser_extension_config_1.field_extractors is None
    assert f'{type(parser_extension_config_1.dynamic_parsing).__module__}.{type(parser_extension_config_1.dynamic_parsing).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    parser_extension_config_2 = module_0.ParserExtensionConfig(str_0, field_extractors=parser_extension_config_1)
    assert f'{type(parser_extension_config_2).__module__}.{type(parser_extension_config_2).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_2.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_2.parser_config is None
    assert f'{type(parser_extension_config_2.field_extractors).__module__}.{type(parser_extension_config_2.field_extractors).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_2.dynamic_parsing is None
    assert parser_extension_config_2.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    parser_extension_config_1.to_dict()

def test_case_8():
    str_0 = 'z2iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    parser_extension_config_1 = module_0.ParserExtensionConfig(str_0, str_0)
    assert f'{type(parser_extension_config_1).__module__}.{type(parser_extension_config_1).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_1.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_1.parser_config == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_1.field_extractors is None
    assert parser_extension_config_1.dynamic_parsing is None
    assert parser_extension_config_1.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert parser_extension_config_1.encoded_cbn_snippet == 'ejJpcUZyLCNdPjtgT3I='
    parser_extension_config_1.to_dict()

def test_case_9():
    str_0 = 'z2iqFr,#]>;`Or'
    parser_extension_config_0 = module_0.ParserExtensionConfig(str_0)
    assert f'{type(parser_extension_config_0).__module__}.{type(parser_extension_config_0).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_0.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_0.parser_config is None
    assert parser_extension_config_0.field_extractors is None
    assert parser_extension_config_0.dynamic_parsing is None
    assert parser_extension_config_0.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    assert module_0.ParserExtensionConfig.log is None
    assert module_0.ParserExtensionConfig.parser_config is None
    assert module_0.ParserExtensionConfig.field_extractors is None
    assert module_0.ParserExtensionConfig.dynamic_parsing is None
    assert module_0.ParserExtensionConfig.encoded_log is None
    assert module_0.ParserExtensionConfig.encoded_cbn_snippet is None
    parser_extension_config_1 = module_0.ParserExtensionConfig(str_0, field_extractors=parser_extension_config_0)
    assert f'{type(parser_extension_config_1).__module__}.{type(parser_extension_config_1).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_1.log == 'z2iqFr,#]>;`Or'
    assert parser_extension_config_1.parser_config is None
    assert f'{type(parser_extension_config_1.field_extractors).__module__}.{type(parser_extension_config_1.field_extractors).__qualname__}' == 'snippet_288.ParserExtensionConfig'
    assert parser_extension_config_1.dynamic_parsing is None
    assert parser_extension_config_1.encoded_log == 'ejJpcUZyLCNdPjtgT3I='
    parser_extension_config_1.to_dict()