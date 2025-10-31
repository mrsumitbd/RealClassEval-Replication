import snippet_252 as module_0

def test_case_0():
    bytes_0 = b'\x16\xbd\x1d\xf3\xd7\x82\xa2\xd7M\x1af\xdd\xe6Ta\x88'
    set_0 = {bytes_0}
    base_plugin_0 = module_0.BasePlugin()
    assert f'{type(base_plugin_0).__module__}.{type(base_plugin_0).__qualname__}' == 'snippet_252.BasePlugin'
    assert module_0.BasePlugin.name == 'BasePlugin'
    base_plugin_0.register_frontend(set_0)

def test_case_1():
    base_plugin_0 = module_0.BasePlugin()
    assert f'{type(base_plugin_0).__module__}.{type(base_plugin_0).__qualname__}' == 'snippet_252.BasePlugin'
    assert module_0.BasePlugin.name == 'BasePlugin'
    base_plugin_0.register_backend(base_plugin_0)
    base_plugin_0.register_frontend(base_plugin_0)