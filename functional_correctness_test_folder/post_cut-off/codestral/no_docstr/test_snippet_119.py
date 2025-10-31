import pytest
import snippet_119 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    str_0 = 'EtOc8\x0c:Q7Cq'
    media_part_0 = module_0.MediaPart(str_0, none_type_0)
    assert f'{type(media_part_0).__module__}.{type(media_part_0).__qualname__}' == 'snippet_119.MediaPart'
    assert media_part_0.base64data == 'EtOc8\x0c:Q7Cq'
    assert media_part_0.mime_type is None
    assert f'{type(module_0.MediaPart.from_json).__module__}.{type(module_0.MediaPart.from_json).__qualname__}' == 'builtins.method'
    media_part_0.is_audio()

def test_case_1():
    str_0 = ']'
    str_1 = '8?F!GL|avlvs>#{NC'
    media_part_0 = module_0.MediaPart(str_0, str_1)
    assert f'{type(media_part_0).__module__}.{type(media_part_0).__qualname__}' == 'snippet_119.MediaPart'
    assert media_part_0.base64data == ']'
    assert media_part_0.mime_type == '8?F!GL|avlvs>#{NC'
    assert f'{type(module_0.MediaPart.from_json).__module__}.{type(module_0.MediaPart.from_json).__qualname__}' == 'builtins.method'
    bool_0 = media_part_0.is_image()
    assert bool_0 is False

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = ']'
    str_1 = '8?F!GL|avlvs>#{NC'
    media_part_0 = module_0.MediaPart(str_0, str_1)
    assert f'{type(media_part_0).__module__}.{type(media_part_0).__qualname__}' == 'snippet_119.MediaPart'
    assert media_part_0.base64data == ']'
    assert media_part_0.mime_type == '8?F!GL|avlvs>#{NC'
    assert f'{type(module_0.MediaPart.from_json).__module__}.{type(module_0.MediaPart.from_json).__qualname__}' == 'builtins.method'
    bool_0 = media_part_0.is_image()
    assert bool_0 is False
    media_part_0.is_config()