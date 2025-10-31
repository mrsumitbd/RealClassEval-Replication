import snippet_306 as module_0

def test_case_0():
    str_0 = 'vobK'
    dict_0 = {str_0: str_0}
    none_type_0 = None
    output_mapping_validator_0 = module_0.OutputMappingValidator()
    assert f'{type(output_mapping_validator_0).__module__}.{type(output_mapping_validator_0).__qualname__}' == 'snippet_306.OutputMappingValidator'
    dict_1 = output_mapping_validator_0.validate_output_mappings(str_0, dict_0, none_type_0)
    assert dict_1 == 'vobK'

def test_case_1():
    output_mapping_validator_0 = module_0.OutputMappingValidator()
    assert f'{type(output_mapping_validator_0).__module__}.{type(output_mapping_validator_0).__qualname__}' == 'snippet_306.OutputMappingValidator'
    dict_0 = {}
    output_mapping_validator_0.validate_output_mappings(dict_0, output_mapping_validator_0, output_mapping_validator_0)