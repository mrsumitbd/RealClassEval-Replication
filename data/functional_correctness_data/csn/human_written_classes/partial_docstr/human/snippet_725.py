import xml.etree.ElementTree

class GlyphData:
    """Map (alternative) names and production names to GlyphData data.

    This class holds the GlyphData data as provided on
    https://github.com/schriftgestalt/GlyphsInfo and provides lookup by
    name, alternative name and production name through normal
    dictionaries.
    """
    __slots__ = ['names', 'alternative_names', 'production_names', 'unicodes']

    def __init__(self, name_mapping, alt_name_mapping, production_name_mapping, unicodes_mapping):
        self.names = name_mapping
        self.alternative_names = alt_name_mapping
        self.production_names = production_name_mapping
        self.unicodes = unicodes_mapping

    @classmethod
    def from_files(cls, *glyphdata_files):
        """Return GlyphData holding data from a list of XML file paths."""
        name_mapping = {}
        alt_name_mapping = {}
        production_name_mapping = {}
        unicodes_mapping = {}
        for glyphdata_file in glyphdata_files:
            glyph_data = xml.etree.ElementTree.parse(glyphdata_file).getroot()
            for glyph in glyph_data:
                glyph_name = glyph.attrib['name']
                glyph_name_alternatives = glyph.attrib.get('altNames')
                glyph_name_production = glyph.attrib.get('production')
                glyph_unicode = glyph.attrib.get('unicode')
                name_mapping[glyph_name] = glyph.attrib
                if glyph_name_alternatives:
                    alternatives = glyph_name_alternatives.replace(' ', '').split(',')
                    for glyph_name_alternative in alternatives:
                        alt_name_mapping[glyph_name_alternative] = glyph.attrib
                if glyph_name_production:
                    production_name_mapping[glyph_name_production] = glyph.attrib
                if glyph_unicode:
                    unicodes_mapping[glyph_unicode] = glyph.attrib
        return cls(name_mapping, alt_name_mapping, production_name_mapping, unicodes_mapping)