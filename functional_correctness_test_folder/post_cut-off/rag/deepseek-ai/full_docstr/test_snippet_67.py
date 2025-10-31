import pytest
import snippet_67 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    str_0 = 'Z8k'
    str_1 = 'd'
    float_0 = -661.46793
    super_chat_record_0 = module_0.SuperChatRecord(none_type_0, str_0, str_0, str_1, float_0, str_0, none_type_0, none_type_0)
    assert f'{type(super_chat_record_0).__module__}.{type(super_chat_record_0).__qualname__}' == 'snippet_67.SuperChatRecord'
    assert super_chat_record_0.user_id is None
    assert super_chat_record_0.user_nickname == 'Z8k'
    assert super_chat_record_0.platform == 'Z8k'
    assert super_chat_record_0.chat_id == 'd'
    assert super_chat_record_0.price == pytest.approx(-661.46793, abs=0.01, rel=0.01)
    assert super_chat_record_0.message_text == 'Z8k'
    assert super_chat_record_0.timestamp is None
    assert super_chat_record_0.expire_time is None
    assert super_chat_record_0.group_name is None
    assert module_0.SuperChatRecord.group_name is None
    super_chat_record_0.is_expired()

def test_case_1():
    str_0 = '_*}L\x0c(lOa&CrcEb_H=D'
    str_1 = 'w,\x0bd$d'
    none_type_0 = None
    str_2 = 'I\tH?(e}l'
    int_0 = 1588
    super_chat_record_0 = module_0.SuperChatRecord(str_0, str_0, str_1, str_1, none_type_0, str_2, int_0, int_0)
    assert f'{type(super_chat_record_0).__module__}.{type(super_chat_record_0).__qualname__}' == 'snippet_67.SuperChatRecord'
    assert super_chat_record_0.user_id == '_*}L\x0c(lOa&CrcEb_H=D'
    assert super_chat_record_0.user_nickname == '_*}L\x0c(lOa&CrcEb_H=D'
    assert super_chat_record_0.platform == 'w,\x0bd$d'
    assert super_chat_record_0.chat_id == 'w,\x0bd$d'
    assert super_chat_record_0.price is None
    assert super_chat_record_0.message_text == 'I\tH?(e}l'
    assert super_chat_record_0.timestamp == 1588
    assert super_chat_record_0.expire_time == 1588
    assert super_chat_record_0.group_name is None
    assert module_0.SuperChatRecord.group_name is None
    float_0 = super_chat_record_0.remaining_time()
    assert float_0 == 0

def test_case_2():
    bool_0 = True
    bytes_0 = b'\x98\xc7\x03eZ\x14\xf6\xdf\xf8f'
    tuple_0 = (bytes_0, bytes_0)
    str_0 = '5yUSW]T\r|K'
    float_0 = -6007.192857
    none_type_0 = None
    super_chat_record_0 = module_0.SuperChatRecord(str_0, tuple_0, bytes_0, str_0, bool_0, str_0, bool_0, float_0, none_type_0)
    assert f'{type(super_chat_record_0).__module__}.{type(super_chat_record_0).__qualname__}' == 'snippet_67.SuperChatRecord'
    assert super_chat_record_0.user_id == '5yUSW]T\r|K'
    assert super_chat_record_0.user_nickname == (b'\x98\xc7\x03eZ\x14\xf6\xdf\xf8f', b'\x98\xc7\x03eZ\x14\xf6\xdf\xf8f')
    assert super_chat_record_0.platform == b'\x98\xc7\x03eZ\x14\xf6\xdf\xf8f'
    assert super_chat_record_0.chat_id == '5yUSW]T\r|K'
    assert super_chat_record_0.price is True
    assert super_chat_record_0.message_text == '5yUSW]T\r|K'
    assert super_chat_record_0.timestamp is True
    assert super_chat_record_0.expire_time == pytest.approx(-6007.192857, abs=0.01, rel=0.01)
    assert super_chat_record_0.group_name is None
    assert module_0.SuperChatRecord.group_name is None
    super_chat_record_0.to_dict()