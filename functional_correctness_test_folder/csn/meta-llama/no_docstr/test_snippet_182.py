import pytest
import snippet_182 as module_0
import PIL.ImagePalette as module_1

def test_case_0():
    blend_0 = module_0.Blend()
    assert f'{type(blend_0).__module__}.{type(blend_0).__qualname__}' == 'snippet_182.Blend'

@pytest.mark.xfail(strict=True)
def test_case_1():
    image_palette_0 = module_1.random()
    assert f'{type(image_palette_0).__module__}.{type(image_palette_0).__qualname__}' == 'PIL.ImagePalette.ImagePalette'
    assert image_palette_0.mode == 'RGB'
    assert image_palette_0.rawmode is None
    assert image_palette_0.dirty is None
    assert f'{type(module_1.annotations).__module__}.{type(module_1.annotations).__qualname__}' == '__future__._Feature'
    assert module_1.annotations.optional == (3, 7, 0, 'beta', 1)
    assert module_1.annotations.mandatory == (3, 11, 0, 'alpha', 0)
    assert module_1.annotations.compiler_flag == 16777216
    assert module_1.TYPE_CHECKING is False
    assert f'{type(module_1.ImagePalette.palette).__module__}.{type(module_1.ImagePalette.palette).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.ImagePalette.colors).__module__}.{type(module_1.ImagePalette.colors).__qualname__}' == 'builtins.property'
    blend_0 = module_0.Blend()
    assert f'{type(blend_0).__module__}.{type(blend_0).__qualname__}' == 'snippet_182.Blend'
    blend_0.overlay(image_palette_0, image_palette_0)