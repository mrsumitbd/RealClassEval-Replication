import pytest
import platform as module_0
import snippet_323 as module_1

def test_case_0():
    var_0 = module_0.python_version_tuple()
    attribute_manager_0 = module_1.AttributeManager(var_0)
    attribute_manager_1 = module_1.AttributeManager(attribute_manager_0)
    str_0 = 'tvr'
    var_1 = attribute_manager_0.determine_entity_category(str_0)
    none_type_0 = None
    var_2 = attribute_manager_1.determine_entity_category(none_type_0)
    dict_0 = attribute_manager_1.prepare_attributes(var_1, var_0, var_1)
    attribute_manager_1.prepare_attributes(var_0, str_0, var_2, dict_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    var_0 = module_0.python_version_tuple()
    attribute_manager_0 = module_1.AttributeManager(var_0)
    str_0 = 'N.M|-p+tH#9C-'
    dict_0 = {str_0: str_0}
    attribute_manager_1 = module_1.AttributeManager(dict_0)
    str_1 = 'tvr'
    var_1 = attribute_manager_0.determine_entity_category(str_1)
    attribute_manager_0.get_gps_attributes(str_0, var_0)
    str_2 = 'H/_YD\x0brY)\n=<'
    attribute_manager_1.prepare_attributes(var_1, str_0, var_1)
    attribute_manager_1.process_json_payload(var_1, str_2)

@pytest.mark.xfail(strict=True)
def test_case_2():
    dict_0 = {}
    attribute_manager_0 = module_1.AttributeManager(dict_0)
    str_0 = 'FX#yRAqv)8L\t'
    attribute_manager_0.determine_entity_category(str_0)
    attribute_manager_0.get_gps_attributes(dict_0, dict_0)

def test_case_3():
    bytes_0 = b'=.\xa7\xd2k'
    module_1.AttributeManager(bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    module_0.freedesktop_os_release()

def test_case_5():
    dict_0 = {}
    attribute_manager_0 = module_1.AttributeManager(dict_0)
    str_0 = 'Fy\t<'
    var_0 = module_0.python_build()
    attribute_manager_0.process_json_payload(str_0, var_0)

def test_case_6():
    none_type_0 = None
    attribute_manager_0 = module_1.AttributeManager(none_type_0)
    str_0 = '/[?/4'
    var_0 = module_0.python_compiler()
    attribute_manager_0.get_gps_attributes(var_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    bytes_0 = b'=.\xa7\xd2k'
    attribute_manager_0 = module_1.AttributeManager(bytes_0)
    str_0 = 'Ov+\\7ck[Y;kszKYh'
    none_type_0 = None
    str_1 = '8|'
    list_0 = [str_0, str_1, str_1]
    attribute_manager_0.prepare_attributes(str_0, none_type_0, list_0, str_1)