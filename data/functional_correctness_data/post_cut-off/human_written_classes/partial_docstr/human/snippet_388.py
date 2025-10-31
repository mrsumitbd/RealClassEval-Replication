from pipask._vendor.pip._internal.models.link import Link
from typing import Iterable, Optional, Tuple
from pipask._vendor.pip._internal.exceptions import NetworkConnectionError
import os
from pipask._vendor.pip._internal.network.session import PipSession

class Downloader:

    def __init__(self, session: PipSession, progress_bar: str) -> None:
        self._session = session
        self._progress_bar = progress_bar

    def __call__(self, link: Link, location: str) -> Tuple[str, str]:
        """Download the file given by link into location."""
        try:
            resp = _http_get_download(self._session, link)
        except NetworkConnectionError as e:
            assert e.response is not None
            logger.critical('HTTP error %s while getting %s', e.response.status_code, link)
            raise
        filename = _get_http_response_filename(resp, link)
        filepath = os.path.join(location, filename)
        chunks = _prepare_download(resp, link, self._progress_bar)
        with open(filepath, 'wb') as content_file:
            for chunk in chunks:
                content_file.write(chunk)
        content_type = resp.headers.get('Content-Type', '')
        return (filepath, content_type)