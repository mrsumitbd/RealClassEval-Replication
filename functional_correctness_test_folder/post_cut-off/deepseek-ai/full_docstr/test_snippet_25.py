import snippet_25 as module_0

def test_case_0():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = 'mm7S\n.xinQQ$1-'
    str_1 = u_r_l_extractor_0.convert_arxiv_url(str_0)
    assert str_1 == 'mm7S\n.xinQQ$1-'

def test_case_1():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = 'unRaJ4\x0cioNK'
    str_1 = u_r_l_extractor_0.infer_filename_from_url(str_0)
    assert str_1 == 'unRaJ4\x0cioNK_20250925_212902.html'

def test_case_2():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = '#]"\t'
    str_1 = u_r_l_extractor_0.convert_arxiv_url(str_0)
    assert str_1 == '#]"\t'
    str_2 = u_r_l_extractor_0.infer_filename_from_url(str_1)
    assert str_2 == '_20250925_212902.html'
    str_3 = '."r6['
    str_4 = u_r_l_extractor_0.convert_arxiv_url(str_3)
    assert str_4 == '."r6['
    str_5 = '9'
    str_6 = u_r_l_extractor_0.infer_filename_from_url(str_5)
    assert str_6 == '9_20250925_212902.html'
    str_7 = u_r_l_extractor_0.infer_filename_from_url(str_4)
    assert str_7 == '."r6['

def test_case_3():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = 'mm7S\n.xinQQ$1-'
    str_1 = u_r_l_extractor_0.convert_arxiv_url(str_0)
    assert str_1 == 'mm7S\n.xinQQ$1-'
    str_2 = u_r_l_extractor_0.infer_filename_from_url(str_1)
    assert str_2 == 'mm7S.xinQQ$1-'

def test_case_4():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = '/'
    str_1 = u_r_l_extractor_0.convert_arxiv_url(str_0)
    assert str_1 == '/'
    str_2 = u_r_l_extractor_0.infer_filename_from_url(str_0)
    assert str_2 == '_20250925_212902.html'

def test_case_5():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = '."r6['
    str_1 = u_r_l_extractor_0.convert_arxiv_url(str_0)
    assert str_1 == '."r6['
    str_2 = '9'
    str_3 = u_r_l_extractor_0.infer_filename_from_url(str_2)
    assert str_3 == '9_20250925_212902.html'
    str_4 = '.SwPmx~95E'
    str_5 = '"*EMpd\\&V/#acK\t]K~\r3'
    str_6 = u_r_l_extractor_0.infer_filename_from_url(str_5)
    assert str_6 == '"*EMpd\\&V_20250925_212902.html'
    str_7 = u_r_l_extractor_0.infer_filename_from_url(str_4)
    assert str_7 == '.SwPmx~95E'

def test_case_6():
    u_r_l_extractor_0 = module_0.URLExtractor()
    assert f'{type(u_r_l_extractor_0).__module__}.{type(u_r_l_extractor_0).__qualname__}' == 'snippet_25.URLExtractor'
    assert module_0.URLExtractor.URL_PATTERNS == ["https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*(?:\\?(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?(?:#(?:[-\\w._~!$&\\'()*+,;=:@/?]|%[\\da-fA-F]{2})*)?", "ftp://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+(?:/(?:[-\\w._~!$&\\'()*+,;=:@]|%[\\da-fA-F]{2})*)*", "(?<!\\S)(?:www\\.)?[-\\w]+(?:\\.[-\\w]+)+/(?:[-\\w._~!$&\\'()*+,;=:@/]|%[\\da-fA-F]{2})+"]
    assert f'{type(module_0.URLExtractor.extract_urls).__module__}.{type(module_0.URLExtractor.extract_urls).__qualname__}' == 'builtins.method'
    str_0 = 'y<9l{!'
    str_1 = u_r_l_extractor_0.infer_filename_from_url(str_0)
    assert str_1 == 'y<9l{!_20250925_212902.html'
    str_2 = '#]"\t'
    str_3 = u_r_l_extractor_0.convert_arxiv_url(str_2)
    assert str_3 == '#]"\t'
    str_4 = u_r_l_extractor_0.infer_filename_from_url(str_2)
    assert str_4 == '_20250925_212902.html'
    str_5 = u_r_l_extractor_0.infer_filename_from_url(str_4)
    assert str_5 == '_20250925_212902.html'
    str_6 = '\\.`s~Ljxy6jQ6\x0bY$ohJ/'
    str_7 = u_r_l_extractor_0.infer_filename_from_url(str_6)
    assert str_7 == '\\.`s~Ljxy6jQ6\x0bY$ohJ_20250925_212902'