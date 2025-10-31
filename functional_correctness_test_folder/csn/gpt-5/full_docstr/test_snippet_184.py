import snippet_184 as module_0

def test_case_0():
    str_0 = 'fj5gQbOH$)'
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    var_0 = encoder_0.needsEncoding(str_0)
    assert var_0 is False

def test_case_1():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    var_0 = encoder_0.needsEncoding(encoder_0)
    assert var_0 is False
    var_1 = encoder_0.decode(encoder_0)
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_184.Encoder'
    var_2 = encoder_0.encode(var_1)
    assert f'{type(var_2).__module__}.{type(var_2).__qualname__}' == 'snippet_184.Encoder'

def test_case_2():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    var_0 = encoder_0.encode(encoder_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_184.Encoder'

def test_case_3():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    var_0 = encoder_0.decode(encoder_0)
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_184.Encoder'

def test_case_4():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    encoder_1 = module_0.Encoder()
    assert f'{type(encoder_1).__module__}.{type(encoder_1).__qualname__}' == 'snippet_184.Encoder'
    var_0 = encoder_0.needsEncoding(encoder_1)
    assert var_0 is False
    str_0 = ':g]`~0|H4\\xO]O^0/'
    var_1 = encoder_1.decode(str_0)
    assert var_1 == ':g]`~0|H4\\xO]O^0/'

def test_case_5():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    encoder_1 = module_0.Encoder()
    assert f'{type(encoder_1).__module__}.{type(encoder_1).__qualname__}' == 'snippet_184.Encoder'
    str_0 = '>PqYLuHl[9c.-|k,&'
    var_0 = encoder_1.decode(str_0)
    assert var_0 == '>PqYLuHl[9c.-|k,&'
    var_1 = encoder_0.needsEncoding(str_0)
    assert var_1 is True

def test_case_6():
    encoder_0 = module_0.Encoder()
    assert f'{type(encoder_0).__module__}.{type(encoder_0).__qualname__}' == 'snippet_184.Encoder'
    assert module_0.Encoder.encodings == (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;'))
    assert module_0.Encoder.decodings == (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&'))
    assert module_0.Encoder.special == ('&', '<', '>', '"', "'")
    var_0 = encoder_0.needsEncoding(encoder_0)
    assert var_0 is False
    str_0 = '|pCZ5k'
    var_1 = encoder_0.decode(str_0)
    assert var_1 == '|pCZ5k'
    var_2 = encoder_0.encode(var_1)
    assert var_2 == '|pCZ5k'