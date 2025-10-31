import pytest
import snippet_62 as module_0

def test_case_0():
    str_0 = '\nHpUouo8.>H\x0bgr.'
    float_0 = 173.384
    dict_0 = {str_0: float_0}
    evaluation_result_0 = module_0.EvaluationResult(dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert f'{type(evaluation_result_0.metrics).__module__}.{type(evaluation_result_0.metrics).__qualname__}' == 'builtins.dict'
    assert len(evaluation_result_0.metrics) == 1
    assert evaluation_result_0.artifacts == {}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    evaluation_result_0.get_artifact_keys()
    int_0 = 115
    evaluation_result_1 = module_0.EvaluationResult(int_0)
    assert f'{type(evaluation_result_1).__module__}.{type(evaluation_result_1).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_1.metrics == 115
    assert evaluation_result_1.artifacts == {}
    int_1 = evaluation_result_0.get_artifact_size(str_0)
    assert int_1 == 0
    int_2 = evaluation_result_1.get_total_artifact_size()
    assert int_2 == 0

def test_case_1():
    none_type_0 = None
    evaluation_result_0 = module_0.EvaluationResult(none_type_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_0.metrics is None
    assert evaluation_result_0.artifacts == {}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    int_0 = evaluation_result_0.get_total_artifact_size()
    assert int_0 == 0

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '@l'
    str_1 = 'U6Z'
    int_0 = -3600
    str_2 = '@Is9\x0bdcVm8E3Y#Zy'
    str_3 = 'FU]:D'
    dict_0 = {str_1: int_0, str_2: int_0, str_3: int_0}
    evaluation_result_0 = module_0.EvaluationResult(dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_0.metrics == {'U6Z': -3600, '@Is9\x0bdcVm8E3Y#Zy': -3600, 'FU]:D': -3600}
    assert evaluation_result_0.artifacts == {}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    evaluation_result_1 = module_0.EvaluationResult(evaluation_result_0)
    assert f'{type(evaluation_result_1).__module__}.{type(evaluation_result_1).__qualname__}' == 'snippet_62.EvaluationResult'
    assert f'{type(evaluation_result_1.metrics).__module__}.{type(evaluation_result_1.metrics).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_1.artifacts == {}
    int_1 = evaluation_result_1.get_artifact_size(str_0)
    assert int_1 == 0
    str_4 = "^A\\S5r&~,fq`v.j's"
    float_0 = -1089.8022398057242
    str_5 = "cMKB/hq':?"
    float_1 = -1874.6
    str_6 = 'DCo|N?,U}7(Q\x0b'
    float_2 = -1506.43
    dict_1 = {str_4: float_0, str_5: float_1, str_6: float_1, str_4: float_2}
    evaluation_result_2 = module_0.EvaluationResult(dict_1, float_0)
    assert f'{type(evaluation_result_2).__module__}.{type(evaluation_result_2).__qualname__}' == 'snippet_62.EvaluationResult'
    assert f'{type(evaluation_result_2.metrics).__module__}.{type(evaluation_result_2.metrics).__qualname__}' == 'builtins.dict'
    assert len(evaluation_result_2.metrics) == 3
    assert evaluation_result_2.artifacts == pytest.approx(-1089.8022398057242, abs=0.01, rel=0.01)
    evaluation_result_2.to_dict()
    evaluation_result_2.get_total_artifact_size()

def test_case_3():
    bool_0 = False
    str_0 = '"_'
    str_1 = ''
    dict_0 = {str_0: bool_0, str_0: bool_0, str_1: bool_0}
    evaluation_result_0 = module_0.EvaluationResult(dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_0.metrics == {'"_': False, '': False}
    assert evaluation_result_0.artifacts == {}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    bool_1 = evaluation_result_0.has_artifacts()
    assert bool_1 is False

def test_case_4():
    str_0 = '\nHpUouo8.>H\x0bgr.'
    float_0 = 173.384
    dict_0 = {str_0: float_0}
    evaluation_result_0 = module_0.EvaluationResult(dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert f'{type(evaluation_result_0.metrics).__module__}.{type(evaluation_result_0.metrics).__qualname__}' == 'builtins.dict'
    assert len(evaluation_result_0.metrics) == 1
    assert evaluation_result_0.artifacts == {}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    evaluation_result_0.get_artifact_keys()
    int_0 = 115
    evaluation_result_1 = module_0.EvaluationResult(int_0)
    assert f'{type(evaluation_result_1).__module__}.{type(evaluation_result_1).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_1.metrics == 115
    assert evaluation_result_1.artifacts == {}
    int_1 = evaluation_result_1.get_total_artifact_size()
    assert int_1 == 0

def test_case_5():
    float_0 = -589.7
    str_0 = 'uv\x0cdJoxp'
    dict_0 = {str_0: str_0, str_0: str_0, str_0: str_0, str_0: str_0}
    evaluation_result_0 = module_0.EvaluationResult(float_0, dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_0.metrics == pytest.approx(-589.7, abs=0.01, rel=0.01)
    assert evaluation_result_0.artifacts == {'uv\x0cdJoxp': 'uv\x0cdJoxp'}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    var_0 = evaluation_result_0.__eq__(float_0)
    dict_1 = {var_0: var_0, var_0: float_0}
    evaluation_result_1 = module_0.EvaluationResult(dict_1, dict_1)
    assert f'{type(evaluation_result_1).__module__}.{type(evaluation_result_1).__qualname__}' == 'snippet_62.EvaluationResult'
    assert f'{type(evaluation_result_1.metrics).__module__}.{type(evaluation_result_1.metrics).__qualname__}' == 'builtins.dict'
    assert len(evaluation_result_1.metrics) == 1
    assert f'{type(evaluation_result_1.artifacts).__module__}.{type(evaluation_result_1.artifacts).__qualname__}' == 'builtins.dict'
    assert len(evaluation_result_1.artifacts) == 1
    int_0 = evaluation_result_1.get_total_artifact_size()
    assert int_0 == 6

def test_case_6():
    str_0 = '0"c+G)>C$A'
    str_1 = ";F3`9cMc(pZ'"
    str_2 = '{_ze0u+<FUMR['
    dict_0 = {str_2: str_0, str_0: str_2, str_2: str_2}
    evaluation_result_0 = module_0.EvaluationResult(str_0, dict_0)
    assert f'{type(evaluation_result_0).__module__}.{type(evaluation_result_0).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_0.metrics == '0"c+G)>C$A'
    assert evaluation_result_0.artifacts == {'{_ze0u+<FUMR[': '{_ze0u+<FUMR[', '0"c+G)>C$A': '{_ze0u+<FUMR['}
    assert f'{type(module_0.EvaluationResult.from_dict).__module__}.{type(module_0.EvaluationResult.from_dict).__qualname__}' == 'builtins.method'
    int_0 = evaluation_result_0.get_artifact_size(str_1)
    assert int_0 == 0
    str_3 = '.v;;/\x0bIw6UVwrp\x0b'
    int_1 = 1869
    dict_1 = {str_3: int_1, str_3: int_1}
    str_4 = ''
    dict_2 = {str_3: str_3, str_4: str_3, str_3: str_3, str_4: str_3}
    evaluation_result_1 = module_0.EvaluationResult(dict_1, dict_2)
    assert f'{type(evaluation_result_1).__module__}.{type(evaluation_result_1).__qualname__}' == 'snippet_62.EvaluationResult'
    assert evaluation_result_1.metrics == {'.v;;/\x0bIw6UVwrp\x0b': 1869}
    assert evaluation_result_1.artifacts == {'.v;;/\x0bIw6UVwrp\x0b': '.v;;/\x0bIw6UVwrp\x0b', '': '.v;;/\x0bIw6UVwrp\x0b'}
    int_2 = evaluation_result_1.get_total_artifact_size()
    assert int_2 == 30
    evaluation_result_1.get_artifact_keys()