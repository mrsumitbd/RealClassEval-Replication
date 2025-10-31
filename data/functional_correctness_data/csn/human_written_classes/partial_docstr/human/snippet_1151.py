class Collection:
    """
    A :term:`SKOS` Collection.
    """
    id = None
    'An id for this Collection within a vocabulary'
    uri = None
    'A proper uri for this Collection'
    type = 'collection'
    "The type of this concept or collection.\n\n    eg. 'collection'\n    "
    concept_scheme = None
    'The :class:`ConceptScheme` this Collection is a part of.'
    labels = []
    'A :class:`lst` of :class:`skosprovider.skos.label` instances.'
    notes = []
    'A :class:`lst` of :class:`skosprovider.skos.Note` instances.'
    sources = []
    'A :class:`lst` of :class:`skosprovider.skos.Source` instances.'
    members = []
    'A :class:`lst` of concept or collection ids.'
    member_of = []
    'A :class:`lst` of collection ids.'
    superordinates = []
    'A :class:`lst` of concept ids.'
    infer_concept_relations = True
    'Should member concepts of this collection be seen as narrower concept of\n    a superordinate of the collection?'

    def __init__(self, id, uri=None, concept_scheme=None, labels=[], notes=[], sources=[], members=[], member_of=[], superordinates=[], infer_concept_relations=True):
        self.id = id
        self.uri = uri
        self.type = 'collection'
        self.concept_scheme = concept_scheme
        self.labels = [dict_to_label(l) for l in labels]
        self.notes = [dict_to_note(n) for n in notes]
        self.sources = [dict_to_source(s) for s in sources]
        self.members = members
        self.member_of = member_of
        self.superordinates = superordinates
        self.infer_concept_relations = infer_concept_relations

    def label(self, language='any'):
        """
        Provide a single label for this collection.

        This uses the :func:`label` function to determine which label to return.

        :param string language: The preferred language to receive the label in.
            This should be a valid IANA language tag.
        :rtype: :class:`skosprovider.skos.Label` or None if no labels were found.
        """
        return label(self.labels, language, False)

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
        return f"Collection('{self.id}')"