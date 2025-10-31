import snippet_4 as module_0

def test_case_0():
    simple_tokenizer_0 = module_0.SimpleTokenizer()
    assert f'{type(simple_tokenizer_0).__module__}.{type(simple_tokenizer_0).__qualname__}' == 'snippet_4.SimpleTokenizer'
    assert f'{type(simple_tokenizer_0.split_pattern).__module__}.{type(simple_tokenizer_0.split_pattern).__qualname__}' == 're.Pattern'

def test_case_1():
    str_0 = '[?G'
    simple_tokenizer_0 = module_0.SimpleTokenizer()
    assert f'{type(simple_tokenizer_0).__module__}.{type(simple_tokenizer_0).__qualname__}' == 'snippet_4.SimpleTokenizer'
    assert f'{type(simple_tokenizer_0.split_pattern).__module__}.{type(simple_tokenizer_0.split_pattern).__qualname__}' == 're.Pattern'
    simple_tokenizer_0.__call__(str_0)

def test_case_2():
    str_0 = '[G]'
    simple_tokenizer_0 = module_0.SimpleTokenizer()
    assert f'{type(simple_tokenizer_0).__module__}.{type(simple_tokenizer_0).__qualname__}' == 'snippet_4.SimpleTokenizer'
    assert f'{type(simple_tokenizer_0.split_pattern).__module__}.{type(simple_tokenizer_0.split_pattern).__qualname__}' == 're.Pattern'
    simple_tokenizer_0.__call__(str_0)

def test_case_3():
    str_0 = '[?G'
    simple_tokenizer_0 = module_0.SimpleTokenizer()
    assert f'{type(simple_tokenizer_0).__module__}.{type(simple_tokenizer_0).__qualname__}' == 'snippet_4.SimpleTokenizer'
    assert f'{type(simple_tokenizer_0.split_pattern).__module__}.{type(simple_tokenizer_0.split_pattern).__qualname__}' == 're.Pattern'
    none_type_0 = None
    simple_tokenizer_0.__call__(str_0, none_type_0)