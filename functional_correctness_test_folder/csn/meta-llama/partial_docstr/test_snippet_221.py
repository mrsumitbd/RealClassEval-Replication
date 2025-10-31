import pytest
import snippet_221 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'B?k>7\t"%jso'
    attachment_0 = module_0.Attachment(str_0, str_0, str_0)
    assert f'{type(attachment_0).__module__}.{type(attachment_0).__qualname__}' == 'snippet_221.Attachment'
    assert attachment_0.file_name == 'B?k>7\t"%jso'
    assert attachment_0.file_type == 'B?k>7\t"%jso'
    assert attachment_0.file_content == 'B?k>7\t"%jso'
    attachment_0.to_dict()

def test_case_1():
    str_0 = 'G|3<_r'
    str_1 = "D'["
    attachment_0 = module_0.Attachment(str_0, str_1, str_1)
    assert f'{type(attachment_0).__module__}.{type(attachment_0).__qualname__}' == 'snippet_221.Attachment'
    assert attachment_0.file_name == 'G|3<_r'
    assert attachment_0.file_type == "D'["
    assert attachment_0.file_content == "D'["
    attachment_0.multipart_form_element()