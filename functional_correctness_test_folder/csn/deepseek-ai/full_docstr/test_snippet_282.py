import pytest
import snippet_282 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    transcript_0 = module_0.Transcript()
    assert f'{type(transcript_0).__module__}.{type(transcript_0).__qualname__}' == 'snippet_282.Transcript'
    assert module_0.Transcript.SRT == 'srt'
    assert module_0.Transcript.SJSON == 'sjson'
    assert f'{type(module_0.Transcript.convert).__module__}.{type(module_0.Transcript.convert).__qualname__}' == 'builtins.method'
    str_0 = 'NuX6U*,*n1W`}p'
    transcript_0.generate_sjson_from_srt(str_0)

def test_case_1():
    dict_0 = {}
    transcript_0 = module_0.Transcript(**dict_0)
    assert f'{type(transcript_0).__module__}.{type(transcript_0).__qualname__}' == 'snippet_282.Transcript'
    assert module_0.Transcript.SRT == 'srt'
    assert module_0.Transcript.SJSON == 'sjson'
    assert f'{type(module_0.Transcript.convert).__module__}.{type(module_0.Transcript.convert).__qualname__}' == 'builtins.method'
    list_0 = []
    var_0 = transcript_0.generate_sjson_from_srt(list_0)
    var_1 = transcript_0.generate_srt_from_sjson(var_0)
    assert var_1 == ''