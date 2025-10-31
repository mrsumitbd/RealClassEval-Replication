from typing import Any, Optional, Dict, Tuple
import pyarrow as pa
import requests
from graphistry.utils.requests import log_requests_error
import sys

class ArrowFileUploader:
    """
        Implement file API with focus on Arrow support

        Memoization in this class is based on reference equality, while plotter is based on hash.
        That means the plotter resolves different-identity value matches, so by the time ArrowFileUploader compares,
        identities are unified for faster reference-based checks.

        Example: Upload files with per-session memoization
            uploader : ArrowUploader
            arr : pa.Table
            afu = ArrowFileUploader(uploader)

            file1_id = afu.create_and_post_file(arr)[0]
            file2_id = afu.create_and_post_file(arr)[0]

            assert file1_id == file2_id # memoizes by default (memory-safe: weak refs)

        Example: Explicitly create a file and upload data for it
            uploader : ArrowUploader
            arr : pa.Table
            afu = ArrowFileUploader(uploader)

            file1_id = afu.create_file()
            afu.post_arrow(arr, file_id)

            file2_id = afu.create_file()
            afu.post_arrow(arr, file_id)

            assert file1_id != file2_id

    """
    uploader: Any = None

    def __init__(self, uploader) -> None:
        self.uploader = uploader

    def create_file(self, file_opts: dict={}) -> str:
        """
            Creates File and returns file_id str.

            Defauls:
              - file_type: 'arrow'

            See File REST API for file_opts
        """
        tok = self.uploader.token
        json_extended = {'file_type': 'arrow', 'agent_name': 'pygraphistry', 'agent_version': sys.modules['graphistry'].__version__, **file_opts}
        res = requests.post(self.uploader.server_base_path + '/api/v2/files/', verify=self.uploader.certificate_validation, headers={'Authorization': f'Bearer {tok}'}, json=json_extended)
        log_requests_error(res)
        try:
            out = res.json()
            logger.debug('Server create file response: %s', out)
            if res.status_code != requests.codes.ok:
                res.raise_for_status()
        except Exception as e:
            logger.error('Failed creating file: %s', res.text, exc_info=True)
            raise e
        return out['file_id']

    def post_arrow(self, arr: pa.Table, file_id: str, url_opts: str='erase=true') -> dict:
        """
            Upload new data to existing file id

            Default url_opts='erase=true' throws exceptions on parse errors and deletes upload.

            See File REST API for url_opts (file upload)
        """
        sub_path = f'api/v2/upload/files/{file_id}'
        tok = self.uploader.token
        res = self.uploader.post_arrow_generic(sub_path, tok, arr, url_opts)
        try:
            out = res.json()
            logger.debug('Server upload file response: %s', out)
            if not out['is_valid']:
                if out['is_uploaded']:
                    raise RuntimeError('Uploaded file contents but cannot parse (file_id still valid), see errors', out['errors'])
                else:
                    raise RuntimeError('Erased uploaded file contents upon failure (file_id still valid), see errors', out['errors'])
            return out
        except Exception as e:
            logger.error('Failed uploading file: %s', res.text, exc_info=True)
            raise e

    def create_and_post_file(self, arr: pa.Table, file_id: Optional[str]=None, file_opts: dict={}, upload_url_opts: str='erase=true', memoize: bool=True) -> Tuple[str, dict]:
        """
        Create a new file (unless `file_id` supplied) and upload `arr`.

        If `memoize` is True (default):

        * Returns a cached `file_id` when there is a hash match for the table,
          in the file_id cache.
        """
        md_hash = _hash_metadata(arr)
        bucket: Optional[Dict[int, Tuple[str, dict]]]
        with _CACHE_LOCK:
            bucket = _CACHE.get(md_hash)
        fh: Optional[int] = None
        if memoize and bucket is not None:
            fh = _hash_full_table(arr)
            with _CACHE_LOCK:
                cached = bucket.get(fh)
                if cached:
                    logger.debug('Memoisation hit (md=%s, full=%s)', md_hash, fh)
                    return cached
        if file_id is None:
            file_id = self.create_file(file_opts)
        resp = self.post_arrow(arr, file_id, upload_url_opts)
        if memoize:
            fh = _hash_full_table(arr) if fh is None else fh
            with _CACHE_LOCK:
                _CACHE.setdefault(md_hash, {})[fh] = (file_id, resp)
                logger.debug('Memoised new upload (md=%s, full=%s)', md_hash, fh)
        return (file_id, resp)