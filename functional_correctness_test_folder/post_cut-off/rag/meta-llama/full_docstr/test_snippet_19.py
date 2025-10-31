import snippet_19 as module_0

def test_case_0():
    str_0 = 'X|\njs}dPppS\x0c('
    markdown_cleaner_0 = module_0.MarkdownCleaner()
    assert f'{type(markdown_cleaner_0).__module__}.{type(markdown_cleaner_0).__qualname__}' == 'snippet_19.MarkdownCleaner'
    assert f'{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__module__}.{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.MarkdownCleaner.REGEXES).__module__}.{type(module_0.MarkdownCleaner.REGEXES).__qualname__}' == 'builtins.list'
    assert len(module_0.MarkdownCleaner.REGEXES) == 12
    str_1 = markdown_cleaner_0.clean_markdown(str_0)
    assert str_1 == '单行表格：X\njs}dPppS\x0c('

def test_case_1():
    str_0 = '|\njs}dPppS\x0c('
    markdown_cleaner_0 = module_0.MarkdownCleaner()
    assert f'{type(markdown_cleaner_0).__module__}.{type(markdown_cleaner_0).__qualname__}' == 'snippet_19.MarkdownCleaner'
    assert f'{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__module__}.{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.MarkdownCleaner.REGEXES).__module__}.{type(module_0.MarkdownCleaner.REGEXES).__qualname__}' == 'builtins.list'
    assert len(module_0.MarkdownCleaner.REGEXES) == 12
    str_1 = markdown_cleaner_0.clean_markdown(str_0)
    assert str_1 == 'js}dPppS\x0c('

def test_case_2():
    markdown_cleaner_0 = module_0.MarkdownCleaner()
    assert f'{type(markdown_cleaner_0).__module__}.{type(markdown_cleaner_0).__qualname__}' == 'snippet_19.MarkdownCleaner'
    assert f'{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__module__}.{type(module_0.MarkdownCleaner.NORMAL_FORMULA_CHARS).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.MarkdownCleaner.REGEXES).__module__}.{type(module_0.MarkdownCleaner.REGEXES).__qualname__}' == 'builtins.list'
    assert len(module_0.MarkdownCleaner.REGEXES) == 12
    str_0 = "eY.2F'Uij<$p~7q\\_$$<"
    str_1 = markdown_cleaner_0.clean_markdown(str_0)
    assert str_1 == "eY.2F'Uij<p~7q\\_$<"