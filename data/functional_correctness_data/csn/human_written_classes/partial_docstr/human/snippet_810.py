from typing import Any, List, Optional, Union

class ClientSideOcrdFile:
    """
    Provides the same interface as :py:class:`ocrd_models.ocrd_file.OcrdFile`
    but without attachment to :py:class:`ocrd_models.ocrd_mets.OcrdMets` since
    this represents the response of the :py:class:`ocrd.mets_server.OcrdMetsServer`.
    """

    def __init__(self, el, mimetype: str='', pageId: str='', loctype: str='OTHER', local_filename: Optional[str]=None, mets: Any=None, url: str='', ID: str='', fileGrp: str=''):
        """
        Args:
            el (): ignored
        Keyword Args:
            mets (): ignored
            mimetype (string): ``@MIMETYPE`` of this ``mets:file``
            pageId (string): ``@ID`` of the physical ``mets:structMap`` entry corresponding to this ``mets:file``
            loctype (string): ``@LOCTYPE`` of this ``mets:file``
            url (string):  ``@xlink:href`` of this ``mets:file`` (if ``@LOCTYPE==URL``)
            local_filename (): ``@xlink:href`` of this ``mets:file`` (if ``@LOCTYPE==FILE @OTHERLOCTYPE==FILE``)
            ID (string): ``@ID`` of this ``mets:file``
        """
        self.ID = ID
        self.mimetype = mimetype
        self.local_filename = local_filename
        self.url = url
        self.loctype = loctype
        self.pageId = pageId
        self.fileGrp = fileGrp

    def __str__(self):
        props = ', '.join(['='.join([k, getattr(self, k) if hasattr(self, k) and getattr(self, k) else '---']) for k in ['fileGrp', 'ID', 'mimetype', 'url', 'local_filename']])
        return '<ClientSideOcrdFile %s]/>' % props