import pytest
import snippet_368 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = ''
    prompt_compiler_0 = module_0.PromptCompiler()
    assert f'{type(prompt_compiler_0).__module__}.{type(prompt_compiler_0).__qualname__}' == 'snippet_368.PromptCompiler'
    assert f'{type(prompt_compiler_0.compiled_dir).__module__}.{type(prompt_compiler_0.compiled_dir).__qualname__}' == 'pathlib.PosixPath'
    prompt_compiler_0.compile(str_0, str_0)

def test_case_1():
    str_0 = 'w0a%\nj'
    prompt_compiler_0 = module_0.PromptCompiler()
    assert f'{type(prompt_compiler_0).__module__}.{type(prompt_compiler_0).__qualname__}' == 'snippet_368.PromptCompiler'
    assert f'{type(prompt_compiler_0.compiled_dir).__module__}.{type(prompt_compiler_0.compiled_dir).__qualname__}' == 'pathlib.PosixPath'
    with pytest.raises(FileNotFoundError):
        prompt_compiler_0.compile(str_0, str_0)

def test_case_2():
    prompt_compiler_0 = module_0.PromptCompiler()
    assert f'{type(prompt_compiler_0).__module__}.{type(prompt_compiler_0).__qualname__}' == 'snippet_368.PromptCompiler'
    assert f'{type(prompt_compiler_0.compiled_dir).__module__}.{type(prompt_compiler_0.compiled_dir).__qualname__}' == 'pathlib.PosixPath'