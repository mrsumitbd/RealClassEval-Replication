import pytest
import snippet_61 as module_0

def test_case_0():
    str_0 = '8M,dQbn'
    program_0 = module_0.Program(str_0, str_0, generation=str_0, metrics=str_0, metadata=str_0)
    assert f'{type(program_0).__module__}.{type(program_0).__qualname__}' == 'snippet_61.Program'
    assert program_0.id == '8M,dQbn'
    assert program_0.code == '8M,dQbn'
    assert program_0.language == 'python'
    assert program_0.parent_id is None
    assert program_0.generation == '8M,dQbn'
    assert program_0.timestamp == pytest.approx(1758854755.6303868, abs=0.01, rel=0.01)
    assert program_0.iteration_found == 0
    assert program_0.metrics == '8M,dQbn'
    assert program_0.complexity == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert program_0.diversity == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert program_0.metadata == '8M,dQbn'
    assert program_0.prompts is None
    assert program_0.artifacts_json is None
    assert program_0.artifact_dir is None
    assert module_0.Program.language == 'python'
    assert module_0.Program.parent_id is None
    assert module_0.Program.generation == 0
    assert module_0.Program.iteration_found == 0
    assert module_0.Program.complexity == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_0.Program.diversity == pytest.approx(0.0, abs=0.01, rel=0.01)
    assert module_0.Program.prompts is None
    assert module_0.Program.artifacts_json is None
    assert module_0.Program.artifact_dir is None
    assert f'{type(module_0.Program.from_dict).__module__}.{type(module_0.Program.from_dict).__qualname__}' == 'builtins.method'
    program_0.to_dict()