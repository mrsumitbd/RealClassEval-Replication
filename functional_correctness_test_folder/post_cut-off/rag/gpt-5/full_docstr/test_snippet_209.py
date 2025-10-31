import pytest
import snippet_209 as module_0
import re as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.DriverAnalyzer(none_type_0)

def test_case_1():
    str_0 = "Kog -t+'\t7"
    regex_flag_0 = module_1.RegexFlag.TEMPLATE
    dict_0 = {regex_flag_0: str_0}
    driver_analyzer_0 = module_0.DriverAnalyzer(dict_0)
    assert f'{type(driver_analyzer_0).__module__}.{type(driver_analyzer_0).__qualname__}' == 'snippet_209.DriverAnalyzer'
    assert driver_analyzer_0.file_contents == {module_1.RegexFlag.TEMPLATE: "Kog -t+'\t7"}
    assert driver_analyzer_0.all_content == "Kog -t+'\t7"
    assert module_1.ASCII == module_1.RegexFlag.ASCII
    assert module_1.A == module_1.RegexFlag.ASCII
    assert module_1.IGNORECASE == module_1.RegexFlag.IGNORECASE
    assert module_1.I == module_1.RegexFlag.IGNORECASE
    assert module_1.LOCALE == module_1.RegexFlag.LOCALE
    assert module_1.L == module_1.RegexFlag.LOCALE
    assert module_1.UNICODE == module_1.RegexFlag.UNICODE
    assert module_1.U == module_1.RegexFlag.UNICODE
    assert module_1.MULTILINE == module_1.RegexFlag.MULTILINE
    assert module_1.M == module_1.RegexFlag.MULTILINE
    assert module_1.DOTALL == module_1.RegexFlag.DOTALL
    assert module_1.S == module_1.RegexFlag.DOTALL
    assert module_1.VERBOSE == module_1.RegexFlag.VERBOSE
    assert module_1.X == module_1.RegexFlag.VERBOSE
    assert module_1.TEMPLATE == module_1.RegexFlag.TEMPLATE
    assert module_1.T == module_1.RegexFlag.TEMPLATE
    assert module_1.DEBUG == module_1.RegexFlag.DEBUG
    driver_analyzer_0.analyze_access_sequences()

def test_case_2():
    str_0 = "Kog -t+'\t7"
    regex_flag_0 = module_1.RegexFlag.TEMPLATE
    dict_0 = {regex_flag_0: str_0}
    driver_analyzer_0 = module_0.DriverAnalyzer(dict_0)
    assert f'{type(driver_analyzer_0).__module__}.{type(driver_analyzer_0).__qualname__}' == 'snippet_209.DriverAnalyzer'
    assert driver_analyzer_0.file_contents == {module_1.RegexFlag.TEMPLATE: "Kog -t+'\t7"}
    assert driver_analyzer_0.all_content == "Kog -t+'\t7"
    assert module_1.ASCII == module_1.RegexFlag.ASCII
    assert module_1.A == module_1.RegexFlag.ASCII
    assert module_1.IGNORECASE == module_1.RegexFlag.IGNORECASE
    assert module_1.I == module_1.RegexFlag.IGNORECASE
    assert module_1.LOCALE == module_1.RegexFlag.LOCALE
    assert module_1.L == module_1.RegexFlag.LOCALE
    assert module_1.UNICODE == module_1.RegexFlag.UNICODE
    assert module_1.U == module_1.RegexFlag.UNICODE
    assert module_1.MULTILINE == module_1.RegexFlag.MULTILINE
    assert module_1.M == module_1.RegexFlag.MULTILINE
    assert module_1.DOTALL == module_1.RegexFlag.DOTALL
    assert module_1.S == module_1.RegexFlag.DOTALL
    assert module_1.VERBOSE == module_1.RegexFlag.VERBOSE
    assert module_1.X == module_1.RegexFlag.VERBOSE
    assert module_1.TEMPLATE == module_1.RegexFlag.TEMPLATE
    assert module_1.T == module_1.RegexFlag.TEMPLATE
    assert module_1.DEBUG == module_1.RegexFlag.DEBUG
    driver_analyzer_0.analyze_timing_constraints()

def test_case_3():
    str_0 = '7'
    dict_0 = {str_0: str_0}
    driver_analyzer_0 = module_0.DriverAnalyzer(dict_0)
    assert f'{type(driver_analyzer_0).__module__}.{type(driver_analyzer_0).__qualname__}' == 'snippet_209.DriverAnalyzer'
    assert driver_analyzer_0.file_contents == {'7': '7'}
    assert driver_analyzer_0.all_content == '7'
    driver_analyzer_0.analyze_function_context(str_0)

def test_case_4():
    bytes_0 = b''
    str_0 = "Kog -t+'\t7"
    regex_flag_0 = module_1.RegexFlag.TEMPLATE
    dict_0 = {bytes_0: str_0, regex_flag_0: str_0}
    driver_analyzer_0 = module_0.DriverAnalyzer(dict_0)
    assert f'{type(driver_analyzer_0).__module__}.{type(driver_analyzer_0).__qualname__}' == 'snippet_209.DriverAnalyzer'
    assert driver_analyzer_0.file_contents == {b'': "Kog -t+'\t7", module_1.RegexFlag.TEMPLATE: "Kog -t+'\t7"}
    assert driver_analyzer_0.all_content == "Kog -t+'\t7\nKog -t+'\t7"
    assert module_1.ASCII == module_1.RegexFlag.ASCII
    assert module_1.A == module_1.RegexFlag.ASCII
    assert module_1.IGNORECASE == module_1.RegexFlag.IGNORECASE
    assert module_1.I == module_1.RegexFlag.IGNORECASE
    assert module_1.LOCALE == module_1.RegexFlag.LOCALE
    assert module_1.L == module_1.RegexFlag.LOCALE
    assert module_1.UNICODE == module_1.RegexFlag.UNICODE
    assert module_1.U == module_1.RegexFlag.UNICODE
    assert module_1.MULTILINE == module_1.RegexFlag.MULTILINE
    assert module_1.M == module_1.RegexFlag.MULTILINE
    assert module_1.DOTALL == module_1.RegexFlag.DOTALL
    assert module_1.S == module_1.RegexFlag.DOTALL
    assert module_1.VERBOSE == module_1.RegexFlag.VERBOSE
    assert module_1.X == module_1.RegexFlag.VERBOSE
    assert module_1.TEMPLATE == module_1.RegexFlag.TEMPLATE
    assert module_1.T == module_1.RegexFlag.TEMPLATE
    assert module_1.DEBUG == module_1.RegexFlag.DEBUG
    driver_analyzer_0.analyze_timing_constraints()
    driver_analyzer_0.analyze_access_sequences()
    str_1 = ''
    str_2 = ''
    driver_analyzer_0.analyze_function_context(str_2)
    driver_analyzer_0.analyze_function_context(str_1)