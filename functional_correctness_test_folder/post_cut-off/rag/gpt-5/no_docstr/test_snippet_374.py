import pytest
import snippet_374 as module_0

def test_case_0():
    channel_iterator_0 = module_0.ChannelIterator()
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 0
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.__next__()
    assert len(channel_iterator_0) == 1

def test_case_1():
    int_0 = 2318
    channel_iterator_0 = module_0.ChannelIterator()
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 0
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.get_channel(int_0)
    assert len(channel_iterator_0) == 2319
    var_1 = channel_iterator_0.__iter__()
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(var_1) == 2319
    var_2 = var_1.__len__()
    assert var_2 == 2319

def test_case_2():
    bool_0 = True
    channel_iterator_0 = module_0.ChannelIterator(bool_0)
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 1
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    channel_iterator_0.__next__()

def test_case_3():
    bool_0 = True
    channel_iterator_0 = module_0.ChannelIterator(bool_0)
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 1
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.get_channel(bool_0)
    assert len(channel_iterator_0) == 2
    channel_iterator_0.__next__()
    channel_iterator_1 = module_0.ChannelIterator(bool_0)
    assert f'{type(channel_iterator_1).__module__}.{type(channel_iterator_1).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_1) == 1
    var_1 = channel_iterator_1.__iter__()
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(var_1) == 1
    var_2 = channel_iterator_0.__len__()
    assert var_2 == 2

@pytest.mark.xfail(strict=True)
def test_case_4():
    float_0 = -2654.0
    bool_0 = True
    channel_iterator_0 = module_0.ChannelIterator(bool_0)
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 1
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.__iter__()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(var_0) == 1
    var_1 = var_0.__iter__()
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(var_1) == 1
    var_1.get_channel(float_0)

def test_case_5():
    channel_iterator_0 = module_0.ChannelIterator()
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 0
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.__iter__()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(var_0) == 0
    var_1 = var_0.__next__()
    assert len(channel_iterator_0) == 1
    assert len(var_0) == 1

def test_case_6():
    channel_iterator_0 = module_0.ChannelIterator()
    assert f'{type(channel_iterator_0).__module__}.{type(channel_iterator_0).__qualname__}' == 'snippet_374.ChannelIterator'
    assert len(channel_iterator_0) == 0
    assert module_0.ChannelIterator.DEFAULT_COLORS == ['FF0000', '00FF00', '0000FF', 'FF00FF', '00FFFF', 'FFFF00', 'FFFFFF']
    var_0 = channel_iterator_0.__next__()
    assert len(channel_iterator_0) == 1
    var_1 = channel_iterator_0.__len__()
    assert var_1 == 1