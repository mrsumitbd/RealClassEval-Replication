import pytest
import snippet_283 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = -1273
    list_0 = [int_0, int_0]
    progress_bar_stream_0 = module_0.ProgressBarStream(list_0)
    assert f'{type(progress_bar_stream_0).__module__}.{type(progress_bar_stream_0).__qualname__}' == 'snippet_283.ProgressBarStream'
    assert progress_bar_stream_0.stream == [-1273, -1273]
    progress_bar_stream_0.flush()

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    progress_bar_stream_0 = module_0.ProgressBarStream(bool_0)
    assert f'{type(progress_bar_stream_0).__module__}.{type(progress_bar_stream_0).__qualname__}' == 'snippet_283.ProgressBarStream'
    assert progress_bar_stream_0.stream is True
    progress_bar_stream_0.write()