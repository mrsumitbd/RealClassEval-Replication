import pytest
import snippet_83 as module_0
import PIL.Image as module_1

def test_case_0():
    module_0.CenterCrop()

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    module_0.CenterCrop(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    center_crop_0 = module_0.CenterCrop()
    center_crop_0.__call__(center_crop_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    center_crop_0 = module_0.CenterCrop()
    var_0 = module_1.Image()
    assert f'{type(module_1.annotations).__module__}.{type(module_1.annotations).__qualname__}' == '__future__._Feature'
    assert module_1.annotations.optional == (3, 7, 0, 'beta', 1)
    assert module_1.annotations.mandatory == (3, 11, 0, 'alpha', 0)
    assert module_1.annotations.compiler_flag == 16777216
    assert module_1.ElementTree is None
    assert f'{type(module_1.logger).__module__}.{type(module_1.logger).__qualname__}' == 'logging.Logger'
    assert module_1.logger.filters == []
    assert module_1.logger.name == 'PIL.Image'
    assert module_1.logger.level == 0
    assert f'{type(module_1.logger.parent).__module__}.{type(module_1.logger.parent).__qualname__}' == 'logging.RootLogger'
    assert module_1.logger.propagate is True
    assert module_1.logger.handlers == []
    assert module_1.logger.disabled is False
    assert f'{type(module_1.logger.manager).__module__}.{type(module_1.logger.manager).__qualname__}' == 'logging.Manager'
    assert module_1.WARN_POSSIBLE_FORMATS is False
    assert module_1.MAX_IMAGE_PIXELS == 89478485
    assert module_1.item == module_1.Quantize.LIBIMAGEQUANT
    assert module_1.FLIP_LEFT_RIGHT == 0
    assert module_1.FLIP_TOP_BOTTOM == 1
    assert module_1.ROTATE_90 == 2
    assert module_1.ROTATE_180 == 3
    assert module_1.ROTATE_270 == 4
    assert module_1.TRANSPOSE == 5
    assert module_1.TRANSVERSE == 6
    assert module_1.AFFINE == 0
    assert module_1.EXTENT == 1
    assert module_1.PERSPECTIVE == 2
    assert module_1.QUAD == 3
    assert module_1.MESH == 4
    assert module_1.NEAREST == 0
    assert module_1.BOX == 4
    assert module_1.BILINEAR == 2
    assert module_1.HAMMING == 5
    assert module_1.BICUBIC == 3
    assert module_1.LANCZOS == 1
    assert module_1.NONE == 0
    assert module_1.ORDERED == 1
    assert module_1.RASTERIZE == 2
    assert module_1.FLOYDSTEINBERG == 3
    assert module_1.WEB == 0
    assert module_1.ADAPTIVE == 1
    assert module_1.MEDIANCUT == 0
    assert module_1.MAXCOVERAGE == 1
    assert module_1.FASTOCTREE == 2
    assert module_1.LIBIMAGEQUANT == 3
    assert module_1.DEFAULT_STRATEGY == 0
    assert module_1.FILTERED == 1
    assert module_1.HUFFMAN_ONLY == 2
    assert module_1.RLE == 3
    assert module_1.FIXED == 4
    assert module_1.TYPE_CHECKING is False
    assert module_1.ID == []
    assert module_1.OPEN == {}
    assert module_1.MIME == {}
    assert module_1.SAVE == {}
    assert module_1.SAVE_ALL == {}
    assert module_1.EXTENSION == {}
    assert module_1.DECODERS == {}
    assert module_1.ENCODERS == {}
    assert module_1.MODES == ['1', 'CMYK', 'F', 'HSV', 'I', 'I;16', 'I;16B', 'I;16L', 'I;16N', 'L', 'LA', 'La', 'LAB', 'P', 'PA', 'RGB', 'RGBA', 'RGBa', 'RGBX', 'YCbCr']
    assert module_1.Image.format is None
    assert module_1.Image.format_description is None
    assert f'{type(module_1.Image.im).__module__}.{type(module_1.Image.im).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.width).__module__}.{type(module_1.Image.width).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.height).__module__}.{type(module_1.Image.height).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.size).__module__}.{type(module_1.Image.size).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.mode).__module__}.{type(module_1.Image.mode).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.readonly).__module__}.{type(module_1.Image.readonly).__qualname__}' == 'builtins.property'
    assert f'{type(module_1.Image.has_transparency_data).__module__}.{type(module_1.Image.has_transparency_data).__qualname__}' == 'builtins.property'
    center_crop_0.__call__(var_0)