import pytest
import pipask._vendor.pip._internal.models.candidate as module_0
import snippet_202 as module_1

def test_case_0():
    set_0 = set()
    list_0 = []
    str_0 = 'XgK%9qR7sG<e3;\x0c['
    none_type_0 = None
    installation_candidate_0 = module_0.InstallationCandidate(str_0, str_0, none_type_0)
    assert f'{type(installation_candidate_0).__module__}.{type(installation_candidate_0).__qualname__}' == 'pipask._vendor.pip._internal.models.candidate.InstallationCandidate'
    assert f'{type(module_0.InstallationCandidate.link).__module__}.{type(module_0.InstallationCandidate.link).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.name).__module__}.{type(module_0.InstallationCandidate.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.version).__module__}.{type(module_0.InstallationCandidate.version).__qualname__}' == 'builtins.member_descriptor'
    with pytest.raises(AssertionError):
        module_1.BestCandidateResult(set_0, list_0, installation_candidate_0)

def test_case_1():
    bytes_0 = b''
    none_type_0 = None
    best_candidate_result_0 = module_1.BestCandidateResult(bytes_0, bytes_0, none_type_0)
    assert f'{type(best_candidate_result_0).__module__}.{type(best_candidate_result_0).__qualname__}' == 'snippet_202.BestCandidateResult'
    assert best_candidate_result_0.best_candidate is None
    assert module_1.TYPE_CHECKING is False
    best_candidate_result_0.iter_all()
    best_candidate_result_0.iter_applicable()

def test_case_2():
    int_0 = -576
    list_0 = [int_0, int_0, int_0]
    none_type_0 = None
    with pytest.raises(AssertionError):
        module_1.BestCandidateResult(list_0, list_0, none_type_0)

def test_case_3():
    str_0 = '^wgeNdZ6fuBd'
    str_1 = "2AS*?0'(O\t+C"
    str_2 = '[r\\!p.L'
    installation_candidate_0 = module_0.InstallationCandidate(str_1, str_2, str_0)
    assert f'{type(installation_candidate_0).__module__}.{type(installation_candidate_0).__qualname__}' == 'pipask._vendor.pip._internal.models.candidate.InstallationCandidate'
    assert f'{type(module_0.InstallationCandidate.link).__module__}.{type(module_0.InstallationCandidate.link).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.name).__module__}.{type(module_0.InstallationCandidate.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.version).__module__}.{type(module_0.InstallationCandidate.version).__qualname__}' == 'builtins.member_descriptor'
    list_0 = [installation_candidate_0, installation_candidate_0, installation_candidate_0, installation_candidate_0]
    best_candidate_result_0 = module_1.BestCandidateResult(list_0, list_0, installation_candidate_0)
    assert f'{type(best_candidate_result_0).__module__}.{type(best_candidate_result_0).__qualname__}' == 'snippet_202.BestCandidateResult'
    assert f'{type(best_candidate_result_0.best_candidate).__module__}.{type(best_candidate_result_0.best_candidate).__qualname__}' == 'pipask._vendor.pip._internal.models.candidate.InstallationCandidate'
    assert module_1.TYPE_CHECKING is False
    best_candidate_result_0.iter_applicable()

def test_case_4():
    str_0 = 'LkBE+L'
    str_1 = 'p>ZBw\x0b;2T('
    tuple_0 = ()
    installation_candidate_0 = module_0.InstallationCandidate(str_0, str_1, tuple_0)
    assert f'{type(installation_candidate_0).__module__}.{type(installation_candidate_0).__qualname__}' == 'pipask._vendor.pip._internal.models.candidate.InstallationCandidate'
    assert f'{type(module_0.InstallationCandidate.link).__module__}.{type(module_0.InstallationCandidate.link).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.name).__module__}.{type(module_0.InstallationCandidate.name).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_0.InstallationCandidate.version).__module__}.{type(module_0.InstallationCandidate.version).__qualname__}' == 'builtins.member_descriptor'
    list_0 = [installation_candidate_0, installation_candidate_0]
    with pytest.raises(AssertionError):
        module_1.BestCandidateResult(tuple_0, list_0, installation_candidate_0)