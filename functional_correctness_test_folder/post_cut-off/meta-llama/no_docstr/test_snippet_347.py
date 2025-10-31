import pytest
import snippet_347 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    message_builder_0 = module_0.MessageBuilder()
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    str_0 = 'KF9S'
    message_builder_0.build_text_message(str_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    dict_0 = {}
    str_0 = '\x0bjdKibA'
    message_builder_0 = module_0.MessageBuilder(**dict_0)
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_0.build_markdown_message(str_0, dict_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    bytes_0 = b'\x01)\xd2\xf4\x11\xca\x88\xce6\tBW_\xc0(\xa8'
    message_builder_0 = module_0.MessageBuilder()
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_0.build_image_message(bytes_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    message_builder_0 = module_0.MessageBuilder()
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_1 = module_0.MessageBuilder()
    assert f'{type(message_builder_1).__module__}.{type(message_builder_1).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_1.build_file_message(message_builder_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = '\t yO"U'
    message_builder_0 = module_0.MessageBuilder()
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_0.build_keyboard_message(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    bool_0 = False
    message_builder_0 = module_0.MessageBuilder()
    assert f'{type(message_builder_0).__module__}.{type(message_builder_0).__qualname__}' == 'snippet_347.MessageBuilder'
    message_builder_0.build_ark_message(bool_0)