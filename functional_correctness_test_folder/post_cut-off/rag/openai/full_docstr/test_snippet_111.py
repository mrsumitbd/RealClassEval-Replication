import pytest
import snippet_111 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    git_diff_tracker_0 = module_0.GitDiffTracker(logger=bool_0, cwd=bool_0)
    assert f'{type(git_diff_tracker_0).__module__}.{type(git_diff_tracker_0).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_0.enabled is False
    assert git_diff_tracker_0.cwd is False
    assert git_diff_tracker_0.initial_git_hash is None
    assert git_diff_tracker_0.session_start_time == pytest.approx(1758862379.097051, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_0.logger).__module__}.{type(git_diff_tracker_0.logger).__qualname__}' == 'logging.Logger'
    git_diff_tracker_1 = module_0.GitDiffTracker(git_diff_tracker_0)
    assert f'{type(git_diff_tracker_1).__module__}.{type(git_diff_tracker_1).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_1.enabled is False
    assert git_diff_tracker_1.cwd is None
    assert git_diff_tracker_1.initial_git_hash is None
    assert git_diff_tracker_1.session_start_time == pytest.approx(1758862379.100609, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_1.logger).__module__}.{type(git_diff_tracker_1.logger).__qualname__}' == 'logging.Logger'
    git_diff_tracker_1.get_diff()
    none_type_0 = None
    dict_0 = {none_type_0: none_type_0, none_type_0: none_type_0}
    list_0 = [dict_0, none_type_0]
    module_0.GitDiffTracker(logger=list_0, cwd=none_type_0)

def test_case_1():
    git_diff_tracker_0 = module_0.GitDiffTracker()
    assert f'{type(git_diff_tracker_0).__module__}.{type(git_diff_tracker_0).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_0.enabled is False
    assert git_diff_tracker_0.cwd is None
    assert git_diff_tracker_0.initial_git_hash is None
    assert git_diff_tracker_0.session_start_time == pytest.approx(1758862379.140864, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_0.logger).__module__}.{type(git_diff_tracker_0.logger).__qualname__}' == 'logging.Logger'

def test_case_2():
    bool_0 = False
    git_diff_tracker_0 = module_0.GitDiffTracker(bool_0)
    assert f'{type(git_diff_tracker_0).__module__}.{type(git_diff_tracker_0).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_0.enabled is False
    assert git_diff_tracker_0.cwd is None
    assert git_diff_tracker_0.initial_git_hash is None
    assert git_diff_tracker_0.session_start_time == pytest.approx(1758862379.163136, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_0.logger).__module__}.{type(git_diff_tracker_0.logger).__qualname__}' == 'logging.Logger'
    git_diff_tracker_0.get_diff()

def test_case_3():
    bool_0 = False
    git_diff_tracker_0 = module_0.GitDiffTracker(logger=bool_0, cwd=bool_0)
    assert f'{type(git_diff_tracker_0).__module__}.{type(git_diff_tracker_0).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_0.enabled is False
    assert git_diff_tracker_0.cwd is False
    assert git_diff_tracker_0.initial_git_hash is None
    assert git_diff_tracker_0.session_start_time == pytest.approx(1758862379.164709, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_0.logger).__module__}.{type(git_diff_tracker_0.logger).__qualname__}' == 'logging.Logger'

def test_case_4():
    git_diff_tracker_0 = module_0.GitDiffTracker()
    assert f'{type(git_diff_tracker_0).__module__}.{type(git_diff_tracker_0).__qualname__}' == 'snippet_111.GitDiffTracker'
    assert git_diff_tracker_0.enabled is False
    assert git_diff_tracker_0.cwd is None
    assert git_diff_tracker_0.initial_git_hash is None
    assert git_diff_tracker_0.session_start_time == pytest.approx(1758862379.167778, abs=0.01, rel=0.01)
    assert f'{type(git_diff_tracker_0.logger).__module__}.{type(git_diff_tracker_0.logger).__qualname__}' == 'logging.Logger'
    git_diff_tracker_0.get_diff()