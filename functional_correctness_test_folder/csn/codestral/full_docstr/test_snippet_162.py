import snippet_162 as module_0

def test_case_0():
    str_0 = 'lOa&CrcEb_H=D!73s'
    str_1 = 'lP;m2)g@Nl6'
    web_v_t_t_comment_block_0 = module_0.WebVTTCommentBlock(str_1)
    assert f'{type(web_v_t_t_comment_block_0).__module__}.{type(web_v_t_t_comment_block_0).__qualname__}' == 'snippet_162.WebVTTCommentBlock'
    assert web_v_t_t_comment_block_0.text == 'lP;m2)g@Nl6'
    assert f'{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__module__}.{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.WebVTTCommentBlock.is_valid).__module__}.{type(module_0.WebVTTCommentBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.WebVTTCommentBlock.from_lines).__module__}.{type(module_0.WebVTTCommentBlock.from_lines).__qualname__}' == 'builtins.method'
    web_v_t_t_comment_block_0.format_lines(str_0)

def test_case_1():
    none_type_0 = None
    web_v_t_t_comment_block_0 = module_0.WebVTTCommentBlock(none_type_0)
    assert f'{type(web_v_t_t_comment_block_0).__module__}.{type(web_v_t_t_comment_block_0).__qualname__}' == 'snippet_162.WebVTTCommentBlock'
    assert web_v_t_t_comment_block_0.text is None
    assert f'{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__module__}.{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.WebVTTCommentBlock.is_valid).__module__}.{type(module_0.WebVTTCommentBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.WebVTTCommentBlock.from_lines).__module__}.{type(module_0.WebVTTCommentBlock.from_lines).__qualname__}' == 'builtins.method'
    str_0 = '%\n'
    web_v_t_t_comment_block_0.format_lines(str_0)

def test_case_2():
    str_0 = '(`\n'
    web_v_t_t_comment_block_0 = module_0.WebVTTCommentBlock(str_0)
    assert f'{type(web_v_t_t_comment_block_0).__module__}.{type(web_v_t_t_comment_block_0).__qualname__}' == 'snippet_162.WebVTTCommentBlock'
    assert web_v_t_t_comment_block_0.text == '(`\n'
    assert f'{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__module__}.{type(module_0.WebVTTCommentBlock.COMMENT_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.WebVTTCommentBlock.is_valid).__module__}.{type(module_0.WebVTTCommentBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.WebVTTCommentBlock.from_lines).__module__}.{type(module_0.WebVTTCommentBlock.from_lines).__qualname__}' == 'builtins.method'