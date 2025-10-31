class Concept:
    """
    A :term:`SKOS` Concept.
    """
    id = None
    'An id for this Concept within a vocabulary\n\n    eg. 12345\n    '
    uri = None
    'A proper uri for this Concept\n\n    eg. `http://id.example.com/skos/trees/1`\n    '
    type = 'concept'
    "The type of this concept or collection.\n\n    eg. 'concept'\n    "
    concept_scheme = None
    'The :class:`ConceptScheme` this Concept is a part of.'
    labels = []
    'A :class:`lst` of :class:`Label` instances.'
    notes = []
    'A :class:`lst` of :class:`Note` instances.'
    sources = []
    'A :class:`lst` of :class:`skosprovider.skos.Source` instances.'
    broader = []
    'A :class:`lst` of concept ids.'
    narrower = []
    'A :class:`lst` of concept ids.'
    related = []
    'A :class:`lst` of concept ids.'
    member_of = []
    'A :class:`lst` of collection ids.'
    subordinate_arrays = []
    'A :class:`list` of collection ids.'
    matches = ({},)
    "\n    A :class:`dictionary`. Each key is a matchtype and contains a :class:`list` of URI's.\n    "
    matchtypes = ['close', 'exact', 'related', 'broad', 'narrow']
    "Matches with Concepts in other ConceptSchemes.\n\n    This dictionary contains a key for each type of Match (close, exact,\n    related, broad, narrow). Attached to each key is a list of URI's.\n    "

    def __init__(self, id, uri=None, concept_scheme=None, labels=[], notes=[], sources=[], broader=[], narrower=[], related=[], member_of=[], subordinate_arrays=[], matches={}):
        self.id = id
        self.uri = uri
        self.type = 'concept'
        self.concept_scheme = concept_scheme
        self.labels = [dict_to_label(l) for l in labels]
        self.notes = [dict_to_note(n) for n in notes]
        self.sources = [dict_to_source(s) for s in sources]
        self.broader = broader
        self.narrower = narrower
        self.related = related
        self.member_of = member_of
        self.subordinate_arrays = subordinate_arrays
        self.matches = {key: [] for key in self.matchtypes}
        self.matches.update(matches)

    def label(self, language='any'):
        """
        Provide a single label for this concept.

        This uses the :func:`label` function to determine which label to return.

        :param string language: The preferred language to receive the label in.
            This should be a valid IANA language tag or a list of language tags.
        :rtype: :class:`skosprovider.skos.Label` or None if no labels were found.
        """
        return label(self.labels, language)

    def _sortkey(self, key='id', language='any'):
        """
        Provide a single sortkey for this collection.

        :param string key: Either `id`, `uri`, `label` or `sortlabel`.
        :param string language: The preferred language to receive the label in
            if key is `label` or `sortlabel`. This should be a valid IANA language tag.
        :rtype: :class:`str`
        """
        if key == 'id':
            return str(self.id)
        elif key == 'uri':
            return self.uri if self.uri else ''
        else:
            l = label(self.labels, language, key == 'sortlabel')
            return l.label.lower() if l else ''

    def __repr__(self):
        return f"Concept('{self.id}')"