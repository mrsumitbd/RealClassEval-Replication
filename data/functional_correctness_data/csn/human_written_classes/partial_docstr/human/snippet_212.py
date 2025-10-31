from io import BytesIO
from typing import Union, Optional
from pathlib import Path

class DownloadableMixin:

    def download(self, to_path: Union[None, str, Path]=None, name: str=None, chunk_size: Union[str, int]='auto', convert_to_pdf: bool=False, output: Optional[BytesIO]=None):
        """ Downloads this file to the local drive. Can download the
        file in chunks with multiple requests to the server.

        :param to_path: a path to store the downloaded file
        :type to_path: str or Path
        :param str name: the name you want the stored file to have.
        :param int chunk_size: number of bytes to retrieve from
         each api call to the server. if auto, files bigger than
         SIZE_THERSHOLD will be chunked (into memory, will be
         however only 1 request)
        :param bool convert_to_pdf: will try to download the converted pdf
         if file extension in ALLOWED_PDF_EXTENSIONS
        :param BytesIO output: (optional) an opened io object to write to.
         if set, the to_path and name will be ignored
        :return: Success / Failure
        :rtype: bool
        """
        if not output:
            if to_path is None:
                to_path = Path()
            elif not isinstance(to_path, Path):
                to_path = Path(to_path)
            if not to_path.exists():
                raise FileNotFoundError('{} does not exist'.format(to_path))
            if name and (not Path(name).suffix) and self.name:
                name = name + Path(self.name).suffix
            name = name or self.name
            if convert_to_pdf:
                to_path = to_path / Path(name).with_suffix('.pdf')
            else:
                to_path = to_path / name
        url = self.build_url(self._endpoints.get('download').format(id=self.object_id))
        try:
            if chunk_size is None:
                stream = False
            elif chunk_size == 'auto':
                if self.size and self.size > SIZE_THERSHOLD:
                    stream = True
                else:
                    stream = False
                chunk_size = None
            elif isinstance(chunk_size, int):
                stream = True
            else:
                raise ValueError("Argument chunk_size must be either 'auto' or any integer number representing bytes")
            params = {}
            if convert_to_pdf:
                if not output:
                    if Path(name).suffix in ALLOWED_PDF_EXTENSIONS:
                        params['format'] = 'pdf'
                else:
                    params['format'] = 'pdf'
            with self.con.get(url, stream=stream, params=params) as response:
                if not response:
                    log.debug('Downloading driveitem Request failed: {}'.format(response.reason))
                    return False

                def write_output(out):
                    if stream:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                out.write(chunk)
                    else:
                        out.write(response.content)
                if output:
                    write_output(output)
                else:
                    with to_path.open(mode='wb') as output:
                        write_output(output)
        except Exception as e:
            log.error('Error downloading driveitem {}. Error: {}'.format(self.name, str(e)))
            return False
        return True