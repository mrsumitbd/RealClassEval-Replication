import xml.etree.ElementTree as ET

class FeedEntry:
    """
    Atom feed entry.

    Parameters
    ----------
    title : str
        Title of the entry
    updated : datetime
        Update date
    link : str, optional
        Link (alternate) for the entry
    content : str, optional
        Body HTML text for the entry.
    id_context : list of str, optional
        Material to generate unique IDs from. Feed readers show each id
        as a separate entry, so if an entry is updated, it appears as
        a new entry only if the id_context changes.
        Default: [title, link, content]
    id_date : datetime
        Date to include in the id.
        Default: same as *updated*

    """

    def __init__(self, title, updated, link=None, content=None, id_context=None, id_date=None):
        self.title = title
        self.link = link
        self.updated = updated
        self.content = content
        self.id_context = id_context
        self.id_date = id_date

    def get_atom(self, id_prefix, language):
        item = ET.Element(f'{ATOM_NS}entry')
        id_context = ['entry']
        if self.id_context is None:
            id_context += [self.title, self.link, self.content]
        else:
            id_context += list(self.id_context)
        if self.id_date is None:
            id_date = self.updated
        else:
            id_date = self.id_date
        el = ET.Element(f'{ATOM_NS}id')
        el.text = _get_id(id_prefix, id_date, id_context)
        item.append(el)
        el = ET.Element(f'{ATOM_NS}title')
        el.attrib[f'{XML_NS}lang'] = language
        el.text = self.title
        item.append(el)
        el = ET.Element(f'{ATOM_NS}updated')
        el.text = self.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
        item.append(el)
        if self.link:
            el = ET.Element(f'{ATOM_NS}link')
            el.attrib[f'{ATOM_NS}href'] = self.link
            item.append(el)
        el = ET.Element(f'{ATOM_NS}content')
        el.attrib[f'{XML_NS}lang'] = language
        if self.content:
            el.text = self.content
            el.attrib[f'{ATOM_NS}type'] = 'html'
        else:
            el.text = ' '
        item.append(el)
        return item