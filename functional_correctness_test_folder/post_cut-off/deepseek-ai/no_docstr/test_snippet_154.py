import pytest
import snippet_154 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    shell_utils_0 = module_0.ShellUtils()
    assert f'{type(shell_utils_0).__module__}.{type(shell_utils_0).__qualname__}' == 'snippet_154.ShellUtils'
    assert module_0.ShellUtils.START_KEYWORDS == ('if', 'for', 'while', 'case', 'until')
    assert module_0.ShellUtils.CONTINUATION_KEYWORDS == ('elif', 'else')
    assert module_0.ShellUtils.END_KEYWORDS == ('fi', 'done', 'esac')
    assert module_0.ShellUtils.END_KEYWORDS_WITH_SEMICOLON == ('fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.ALL_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'fi', 'done', 'esac', 'fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.SIMPLE_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'do', 'then')
    assert module_0.ShellUtils.OPERATORS == ('&&', '||', ';', '|', '>', '<', '>>', '<<', '$(', '`')
    str_0 = 'iw.bx'
    bool_0 = shell_utils_0.is_shell_control_end(str_0)
    assert bool_0 is False
    str_1 = "dz2B;!)( \n{HG@1?dM'P"
    bool_1 = shell_utils_0.is_shell_control_start(str_1)
    assert bool_1 is False
    shell_utils_0.contains_shell_operators(shell_utils_0)

def test_case_1():
    shell_utils_0 = module_0.ShellUtils()
    assert f'{type(shell_utils_0).__module__}.{type(shell_utils_0).__qualname__}' == 'snippet_154.ShellUtils'
    assert module_0.ShellUtils.START_KEYWORDS == ('if', 'for', 'while', 'case', 'until')
    assert module_0.ShellUtils.CONTINUATION_KEYWORDS == ('elif', 'else')
    assert module_0.ShellUtils.END_KEYWORDS == ('fi', 'done', 'esac')
    assert module_0.ShellUtils.END_KEYWORDS_WITH_SEMICOLON == ('fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.ALL_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'fi', 'done', 'esac', 'fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.SIMPLE_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'do', 'then')
    assert module_0.ShellUtils.OPERATORS == ('&&', '||', ';', '|', '>', '<', '>>', '<<', '$(', '`')
    str_0 = '6g0l9j*Bz\r<ej,'
    bool_0 = shell_utils_0.is_shell_control_end(str_0)
    assert bool_0 is False

def test_case_2():
    shell_utils_0 = module_0.ShellUtils()
    assert f'{type(shell_utils_0).__module__}.{type(shell_utils_0).__qualname__}' == 'snippet_154.ShellUtils'
    assert module_0.ShellUtils.START_KEYWORDS == ('if', 'for', 'while', 'case', 'until')
    assert module_0.ShellUtils.CONTINUATION_KEYWORDS == ('elif', 'else')
    assert module_0.ShellUtils.END_KEYWORDS == ('fi', 'done', 'esac')
    assert module_0.ShellUtils.END_KEYWORDS_WITH_SEMICOLON == ('fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.ALL_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'fi', 'done', 'esac', 'fi;', 'done;', 'esac;')
    assert module_0.ShellUtils.SIMPLE_KEYWORDS == ('if', 'for', 'while', 'case', 'until', 'elif', 'else', 'do', 'then')
    assert module_0.ShellUtils.OPERATORS == ('&&', '||', ';', '|', '>', '<', '>>', '<<', '$(', '`')
    str_0 = '6g0l9j*Bz\r<ej,'
    bool_0 = shell_utils_0.is_shell_control_end(str_0)
    assert bool_0 is False
    str_1 = '\nL/9:='
    bool_1 = shell_utils_0.contains_shell_operators(str_1)
    assert bool_1 is False