import pytest
import snippet_155 as module_0

def test_case_0():
    str_0 = '^)d6 h'
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    int_0 = pattern_utils_0.get_conditional_indent_level(str_0)
    assert int_0 == 2

def test_case_1():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '?H]dx$7K{i_'
    pattern_utils_0.format_target_colon(str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '[K\x0c$9QaI)oz7}JXm}FS.'
    var_0 = pattern_utils_0.format_target_colon(str_0)
    str_1 = 'r\'n""rJ:p'
    var_1 = pattern_utils_0.format_target_colon(str_1, space_after=pattern_utils_0)
    assert var_1 == 'r\'n""rJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    str_2 = 'Q;H&/5'
    var_2 = pattern_utils_0.format_target_colon(var_1, str_2, bool_0)
    assert var_2 == 'r\'n""rJ :p'
    bool_1 = True
    pattern_utils_0.apply_assignment_spacing(var_0, bool_1)

def test_case_3():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '?H]dx$7K{i_'
    pattern_utils_0.format_pattern_rule(str_0)
    int_0 = pattern_utils_0.get_conditional_indent_level(str_0)
    assert int_0 == 2

@pytest.mark.xfail(strict=True)
def test_case_4():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '?H]dx$7K{i_'
    pattern_utils_0.format_pattern_rule(str_0)
    int_0 = pattern_utils_0.get_conditional_indent_level(str_0)
    assert int_0 == 2
    pattern_utils_0.apply_assignment_spacing(int_0)

def test_case_5():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '?H]dx$7K{i_'
    pattern_utils_0.format_pattern_rule(str_0)
    int_0 = pattern_utils_0.get_conditional_indent_level(str_0)
    assert int_0 == 2
    bool_0 = False
    str_1 = 'q6\x0cq]j]B-q^.rp&HK~z'
    str_2 = pattern_utils_0.apply_assignment_spacing(str_1, bool_0)
    assert str_2 == 'q6\x0cq]j]B-q^.rp&HK~z'

@pytest.mark.xfail(strict=True)
def test_case_6():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_0.is_conditional_directive(pattern_utils_0)

@pytest.mark.xfail(strict=True)
def test_case_7():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = 'T!r\np<!/=8Bk@pN'
    bool_0 = pattern_utils_0.contains_assignment(str_0)
    assert bool_0 is True
    none_type_0 = None
    str_1 = '?H]dx$7K{'
    str_2 = 'oip\r4'
    bool_1 = True
    pattern_utils_1.format_target_colon(str_2, space_after=bool_1)
    pattern_utils_0.format_pattern_rule(str_0)
    int_0 = pattern_utils_0.get_conditional_indent_level(str_1)
    assert int_0 == 2
    pattern_utils_0.apply_assignment_spacing(none_type_0)

def test_case_8():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = 'r+=n\tJ:'
    pattern_utils_0.format_target_colon(str_0, space_after=pattern_utils_1)
    str_1 = 'H*ts4.kx}>T5tP#8X)L_'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    str_2 = 'Z0&#j'
    pattern_utils_0.format_pattern_rule(str_2)

def test_case_9():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '[K\x0c$9QvI)oz7qJXm}FS.'
    pattern_utils_0.format_target_colon(str_0, space_after=pattern_utils_0)
    str_1 = 'Q;H&/5'
    int_0 = pattern_utils_0.get_conditional_indent_level(str_1)
    assert int_0 == 2
    str_2 = pattern_utils_0.apply_assignment_spacing(str_1)
    assert str_2 == 'Q;H&/5'
    str_3 = "%T3\x0cr`FxL(s:'V"
    var_0 = pattern_utils_0.format_pattern_rule(str_3)
    assert var_0 == "%T3\x0cr`FxL(s: 'V"
    pattern_utils_0.format_target_colon(var_0)

def test_case_10():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_0, space_after=pattern_utils_0)
    assert var_0 == 'r\'n"\trJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_0)
    assert bool_0 is False
    str_1 = 'Q;H&/5'
    int_0 = pattern_utils_0.get_conditional_indent_level(var_0)
    assert int_0 == 2
    str_2 = pattern_utils_0.apply_assignment_spacing(str_1)
    assert str_2 == 'Q;H&/5'
    var_1 = pattern_utils_0.format_target_colon(var_0, str_1, bool_0)
    assert var_1 == 'r\'n"\trJ :p'
    str_3 = 'rcn"\trJ: p'
    pattern_utils_0.format_target_colon(str_3, bool_0)

def test_case_11():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '[K\x0c$9QvI)oz7qJXm}FS.'
    pattern_utils_0.format_target_colon(str_0)
    str_1 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_1, space_after=pattern_utils_0)
    assert var_0 == 'r\'n"\trJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    int_0 = pattern_utils_0.get_conditional_indent_level(var_0)
    assert int_0 == 2
    str_2 = pattern_utils_0.apply_assignment_spacing(str_0)
    assert str_2 == '[K\x0c$9QvI)oz7qJXm}FS.'
    var_1 = pattern_utils_0.format_pattern_rule(var_0)
    var_2 = pattern_utils_0.format_target_colon(var_0, var_1, bool_0)
    assert var_2 == 'r\'n"\trJ:p'
    str_3 = '=R5%D6\x0c'
    str_4 = pattern_utils_0.apply_assignment_spacing(str_3)
    assert str_4 == ' = R5%D6\x0c'

def test_case_12():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = 'r\'n\\\t"J:\np'
    pattern_utils_1.format_target_colon(str_0)
    str_1 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_1, space_after=pattern_utils_1)
    assert var_0 == 'r\'n"\trJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    str_2 = 'Q;H&/5'
    int_0 = pattern_utils_0.get_conditional_indent_level(var_0)
    assert int_0 == 2
    str_3 = pattern_utils_1.apply_assignment_spacing(str_2)
    assert str_3 == 'Q;H&/5'
    str_4 = '&WOmP>J\n6B9@&r,Jbvt'
    pattern_utils_0.format_target_colon(str_4)
    pattern_utils_0.format_pattern_rule(str_4)
    str_5 = pattern_utils_0.apply_assignment_spacing(str_4, bool_0)
    assert str_5 == '&WOmP>J\n6B9@&r,Jbvt'

def test_case_13():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = 'b\'n"\trJ:\n'
    var_0 = pattern_utils_0.format_target_colon(str_0, space_after=pattern_utils_1)
    assert var_0 == 'b\'n"\trJ:'
    str_1 = '|l8F%\\lPL'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    int_0 = pattern_utils_1.get_conditional_indent_level(str_1)
    assert int_0 == 2
    str_2 = '&WOmP>J\n6B9@&r,Jbvt'
    str_3 = 'L`;818Nc@#e-\x0b8N5/:'
    pattern_utils_0.format_pattern_rule(str_3)
    str_4 = pattern_utils_1.apply_assignment_spacing(str_2)
    assert str_4 == '&WOmP>J\n6B9@&r,Jbvt'

def test_case_14():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = '[K\x0c$9QaI)oz7}JXm}FS.'
    str_1 = 'KBO?a;;Mv#sa[\\@B[3WV'
    str_2 = pattern_utils_1.apply_assignment_spacing(str_1, pattern_utils_1)
    assert str_2 == 'KBO?a;;Mv#sa[\\@B[3WV'
    pattern_utils_1.format_target_colon(str_0)
    str_3 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_3, space_after=pattern_utils_1)
    assert var_0 == 'r\'n"\trJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_3)
    assert bool_0 is False
    int_0 = pattern_utils_0.get_conditional_indent_level(var_0)
    assert int_0 == 2
    str_4 = '&WOmP>J\n6B9&r,Jbvt'
    pattern_utils_0.format_pattern_rule(str_4)
    str_5 = '\t'
    pattern_utils_1.format_target_colon(str_5, space_after=str_1)

def test_case_15():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    pattern_utils_1 = module_0.PatternUtils()
    assert f'{type(pattern_utils_1).__module__}.{type(pattern_utils_1).__qualname__}' == 'snippet_155.PatternUtils'
    str_0 = '[K\x0c$9QaI)oz7}JXm}FS.'
    pattern_utils_1.format_target_colon(str_0)
    str_1 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_1, space_after=pattern_utils_1)
    assert var_0 == 'r\'n"\trJ: p'
    bool_0 = pattern_utils_0.contains_assignment(str_1)
    assert bool_0 is False
    str_2 = 'Q;H&/5'
    int_0 = pattern_utils_0.get_conditional_indent_level(var_0)
    assert int_0 == 2
    str_3 = pattern_utils_1.apply_assignment_spacing(str_2)
    assert str_3 == 'Q;H&/5'
    str_4 = '&WOmP>J\n6B9&r,Jbvt'
    pattern_utils_0.format_pattern_rule(str_4)
    var_1 = pattern_utils_1.format_target_colon(var_0, str_2, bool_0)
    assert var_1 == 'r\'n"\trJ :p'
    str_5 = 'a\x0boFNL%\n:vF:'
    pattern_utils_0.format_target_colon(str_5)

@pytest.mark.xfail(strict=True)
def test_case_16():
    pattern_utils_0 = module_0.PatternUtils()
    assert f'{type(pattern_utils_0).__module__}.{type(pattern_utils_0).__qualname__}' == 'snippet_155.PatternUtils'
    assert module_0.PatternUtils.ASSIGNMENT_PATTERNS == {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}
    str_0 = '[K\x0c$9QvI)oz7qJXm}FS.'
    bool_0 = False
    str_1 = pattern_utils_0.apply_assignment_spacing(str_0, bool_0)
    assert str_1 == '[K\x0c$9QvI)oz7qJXm}FS.'
    pattern_utils_0.format_target_colon(str_0)
    str_2 = 'r\'n"\trJ:p'
    var_0 = pattern_utils_0.format_target_colon(str_2, space_after=pattern_utils_0)
    assert var_0 == 'r\'n"\trJ: p'
    bool_1 = pattern_utils_0.contains_assignment(str_2)
    assert bool_1 is False
    none_type_0 = None
    pattern_utils_0.format_pattern_rule(str_0)
    str_3 = 'wHRF:'
    pattern_utils_0.format_target_colon(str_3, space_after=bool_0)
    pattern_utils_0.apply_assignment_spacing(none_type_0)