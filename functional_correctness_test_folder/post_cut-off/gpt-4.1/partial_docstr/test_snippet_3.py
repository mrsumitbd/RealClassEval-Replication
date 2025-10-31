import pytest
import dataclasses as module_0
import snippet_3 as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'Gt^IMZgdBP>5j\\6.3;{:'
    str_1 = "Kkv'rTnKS|"
    set_0 = {str_1}
    dict_0 = {str_0: str_0, str_0: set_0}
    str_2 = 'X\x0ca2"4C~4'
    none_type_0 = None
    var_0 = module_0.dataclass(repr=dict_0, order=str_0, kw_only=str_2)
    assert f'{type(module_0.MISSING).__module__}.{type(module_0.MISSING).__qualname__}' == 'dataclasses._MISSING_TYPE'
    assert f'{type(module_0.KW_ONLY).__module__}.{type(module_0.KW_ONLY).__qualname__}' == 'dataclasses._KW_ONLY_TYPE'
    var_1 = var_0.__repr__()
    var_2 = var_1.__eq__(str_0)
    assert var_2 is False
    var_3 = var_2.__eq__(dict_0)
    var_4 = var_3.__eq__(none_type_0)
    var_5 = var_4.__repr__()
    assert var_5 == 'NotImplemented'
    status_bio_d_t_o_0 = module_1.StatusBioDTO(str_0, str_1, dict_0, str_2, none_type_0, var_5)
    assert f'{type(status_bio_d_t_o_0).__module__}.{type(status_bio_d_t_o_0).__qualname__}' == 'snippet_3.StatusBioDTO'
    assert status_bio_d_t_o_0.content == 'Gt^IMZgdBP>5j\\6.3;{:'
    assert status_bio_d_t_o_0.content_third_view == "Kkv'rTnKS|"
    assert status_bio_d_t_o_0.summary == {'Gt^IMZgdBP>5j\\6.3;{:': {"Kkv'rTnKS|"}}
    assert status_bio_d_t_o_0.summary_third_view == 'X\x0ca2"4C~4'
    assert status_bio_d_t_o_0.create_time is None
    assert status_bio_d_t_o_0.update_time == 'NotImplemented'
    assert f'{type(module_1.StatusBioDTO.from_model).__module__}.{type(module_1.StatusBioDTO.from_model).__qualname__}' == 'builtins.method'
    status_bio_d_t_o_0.to_dict()