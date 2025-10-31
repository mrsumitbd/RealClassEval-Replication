class ClientSideOcrdAgent:
    """
    Provides the same interface as :py:class:`ocrd_models.ocrd_file.OcrdAgent`
    but without attachment to :py:class:`ocrd_models.ocrd_mets.OcrdMets` since
    this represents the response of the :py:class:`ocrd.mets_server.OcrdMetsServer`.
    """

    def __init__(self, el, name=None, _type=None, othertype=None, role=None, otherrole=None, notes=None):
        """
        Args:
            el (): ignored
        Keyword Args:
            name (string):
            _type (string):
            othertype (string):
            role (string):
            otherrole (string):
            notes (dict):
        """
        self.name = name
        self.type = _type
        self.othertype = othertype
        self.role = role
        self.otherrole = otherrole
        self.notes = notes

    def __str__(self):
        props = ', '.join(['='.join([k, getattr(self, k) if getattr(self, k) else '---']) for k in ['type', 'othertype', 'role', 'otherrole', 'name']])
        return '<ClientSideOcrdAgent [' + props + ']/>'