import pytest
import snippet_90 as module_0
import PIL.Image as module_1
import numpy as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    module_0.LoadPilAndNumpy(none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    image_0 = module_1.Image()
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
    module_0.LoadPilAndNumpy(image_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    image_0 = module_2.__dir__()
    assert f'{type(module_2.False_).__module__}.{type(module_2.False_).__qualname__}' == 'numpy.bool'
    assert f'{type(module_2.ScalarType).__module__}.{type(module_2.ScalarType).__qualname__}' == 'builtins.tuple'
    assert len(module_2.ScalarType) == 31
    assert f'{type(module_2.True_).__module__}.{type(module_2.True_).__qualname__}' == 'numpy.bool'
    assert module_2.e == pytest.approx(2.718281828459045, abs=0.01, rel=0.01)
    assert module_2.euler_gamma == pytest.approx(0.5772156649015329, abs=0.01, rel=0.01)
    assert module_2.inf == pytest.approx(1e309, abs=0.01, rel=0.01)
    assert module_2.little_endian is True
    assert module_2.newaxis is None
    assert module_2.pi == pytest.approx(3.141592653589793, abs=0.01, rel=0.01)
    assert f'{type(module_2.sctypeDict).__module__}.{type(module_2.sctypeDict).__qualname__}' == 'builtins.dict'
    assert len(module_2.sctypeDict) == 52
    assert module_2.typecodes == {'Character': 'c', 'Integer': 'bhilqnp', 'UnsignedInteger': 'BHILQNP', 'Float': 'efdg', 'Complex': 'FDG', 'AllInteger': 'bBhHiIlLqQnNpP', 'AllFloat': 'efdgFDG', 'Datetime': 'Mm', 'All': '?bhilqnpBHILQNPefdgFDGSUVOMm'}
    assert f'{type(module_2.c_).__module__}.{type(module_2.c_).__qualname__}' == 'numpy.lib._index_tricks_impl.CClass'
    assert len(module_2.c_) == 0
    assert f'{type(module_2.r_).__module__}.{type(module_2.r_).__qualname__}' == 'numpy.lib._index_tricks_impl.RClass'
    assert len(module_2.r_) == 0
    assert f'{type(module_2.s_).__module__}.{type(module_2.s_).__qualname__}' == 'numpy.lib._index_tricks_impl.IndexExpression'
    assert f'{type(module_2.ogrid).__module__}.{type(module_2.ogrid).__qualname__}' == 'numpy.lib._index_tricks_impl.OGridClass'
    assert f'{type(module_2.mgrid).__module__}.{type(module_2.mgrid).__qualname__}' == 'numpy.lib._index_tricks_impl.MGridClass'
    assert f'{type(module_2.index_exp).__module__}.{type(module_2.index_exp).__qualname__}' == 'numpy.lib._index_tricks_impl.IndexExpression'
    module_0.LoadPilAndNumpy(image_0)