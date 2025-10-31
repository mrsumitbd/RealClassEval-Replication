import snippet_243 as module_0

def test_case_0():
    str_0 = 'XFPz$.SPCcfqD;5Y_Q'
    print_and_flush_sink_0 = module_0.PrintAndFlushSink()
    assert f'{type(print_and_flush_sink_0).__module__}.{type(print_and_flush_sink_0).__qualname__}' == 'snippet_243.PrintAndFlushSink'
    print_and_flush_sink_0.write(str_0)

def test_case_1():
    print_and_flush_sink_0 = module_0.PrintAndFlushSink()
    assert f'{type(print_and_flush_sink_0).__module__}.{type(print_and_flush_sink_0).__qualname__}' == 'snippet_243.PrintAndFlushSink'
    print_and_flush_sink_0.flush()