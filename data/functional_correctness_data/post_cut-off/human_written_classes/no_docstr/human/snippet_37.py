from xml.etree.ElementTree import Element

class _AssetData:

    def __init__(self, element: Element, captions: list[Element]):
        self.element = element
        self.line_id: int | None = None
        self._captions: list[Element] = captions
        self._hash: str | None = element.attrib.pop('hash', None)
        if element.tag == 'figure':
            element.clear()
            element.append(self._create_line('[[OCR recognized figure here]]'))
        elif element.tag == 'table':
            element.clear()
            element.append(self._create_line('[[OCR recognized table here]]'))
        elif element.tag == 'formula':
            latex_element = element.find('latex')
            line_text = '[[OCR recognized formula here]]'
            if latex_element is not None and latex_element.text:
                line_text = latex_element.text
            element.clear()
            element.append(self._create_line(line_text))

    def to_saved_xml(self) -> Element:
        asset_element = Element(self.element.tag)
        if asset_element.tag == 'formula':
            line_element = self.element.find('line')
            if line_element is not None:
                latex_element = Element('latex')
                latex_element.text = line_element.text
                asset_element.append(latex_element)
        for raw_caption_element in self._captions:
            caption_element = Element('caption')
            caption_element.extend(raw_caption_element)
            asset_element.append(caption_element)
        if self._hash is not None:
            asset_element.set('hash', self._hash)
        return asset_element

    def _create_line(self, text: str) -> Element:
        line_element = Element('line')
        line_element.text = text
        line_element.attrib['confidence'] = '1.0'
        return line_element