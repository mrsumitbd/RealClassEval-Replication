from ufo2ft.util import _GlyphSet, _hasOverflowingComponentTransforms, zip_strict

class BasePreProcessor:
    """Base class for objects that performs pre-processing operations on
    the UFO glyphs, such as decomposing composites, removing overlaps, or
    applying custom filters.

    By default the input UFO is **not** modified. The ``process`` method
    returns a dictionary containing the new modified glyphset, keyed by
    glyph name. If ``inplace`` is True, the input UFO is modified directly
    without the need to first copy the glyphs.

    Subclasses can override the ``initDefaultFilters`` method and return
    a list of built-in filters which are performed in a predefined order,
    between the user-defined pre- and post-filters.
    The extra kwargs passed to the constructor can be used to customize the
    initialization of the default filters.

    Custom filters can be applied before or after the default filters.
    These can be specified in the UFO lib.plist under the private key
    "com.github.googlei18n.ufo2ft.filters".
    Alternatively the optional ``filters`` parameter can be used. This is a
    list of filter instances (subclasses of BaseFilter) that overrides
    those defined in the UFO lib. The list can be empty, meaning no custom
    filters are run. If ``filters`` contain the special value ``...`` (i.e.
    the actual ``ellipsis`` singleton, not the str literal '...'), then all
    the filters from the UFO lib are loaded in its place. This allows to
    insert additional filters before or after those already defined in the
    UFO lib, as opposed to discard/replace them which is the default behavior
    when ``...`` is absent.
    """

    def __init__(self, ufo, inplace=False, layerName=None, skipExportGlyphs=None, filters=None, **kwargs):
        self.ufo = ufo
        self.inplace = inplace
        self.layerName = layerName
        self.glyphSet = _GlyphSet.from_layer(ufo, layerName, copy=not inplace, skipExportGlyphs=skipExportGlyphs)
        self.defaultFilters = self.initDefaultFilters(**kwargs)
        filters = _load_custom_filters(ufo, filters)
        self.preFilters = [f for f in filters if f.pre]
        self.postFilters = [f for f in filters if not f.pre]

    def initDefaultFilters(self, **kwargs):
        return []

    def process(self):
        ufo = self.ufo
        glyphSet = self.glyphSet
        for func in self.preFilters + self.defaultFilters + self.postFilters:
            func(ufo, glyphSet)
        return glyphSet