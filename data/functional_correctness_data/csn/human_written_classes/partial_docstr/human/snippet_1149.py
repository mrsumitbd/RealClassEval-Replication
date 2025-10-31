import collections.abc
from pycldf.util import pkg_path, resolve_slices, DictTuple, sanitize_url, iter_uritemplates
from clldutils.path import git_describe, walk
import pathlib
import typing
import collections

class GitRepository:
    """
    CLDF datasets are often created from data curated in git repositories. If this is the case, we
    exploit this to provide better provenance information in the dataset's metadata.
    """

    def __init__(self, url: str, clone: typing.Optional[typing.Union[str, pathlib.Path]]=None, version: typing.Optional[str]=None, **dc):
        self.url = sanitize_url(url)
        self.clone = clone
        self.version = version
        self.dc = dc

    def json_ld(self) -> typing.Dict[str, str]:
        res = collections.OrderedDict([('rdf:about', self.url), ('rdf:type', 'prov:Entity')])
        if self.version:
            res['dc:created'] = self.version
        elif self.clone:
            res['dc:created'] = git_describe(self.clone)
        res.update({'dc:{0}'.format(k): self.dc[k] for k in sorted(self.dc)})
        return res