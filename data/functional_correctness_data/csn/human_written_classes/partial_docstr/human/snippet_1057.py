from sirmordred.error import GithubFileNotFound
import urllib.request

class Github:

    def __init__(self, token):
        self.token = token

    def __check_looks_like_uri(self, uri):
        """Checks the URI looks like a RAW uri in github:

        - 'https://raw.githubusercontent.com/github/hubot/master/README.md'
        - 'https://github.com/github/hubot/raw/master/README.md'

        :param uri: uri of the file
        """
        if uri.split('/')[2] == 'raw.githubusercontent.com':
            return True
        elif uri.split('/')[2] == 'github.com':
            if uri.split('/')[5] == 'raw':
                return True
        else:
            raise GithubFileNotFound('URI %s is not a valid link to a raw file in Github' % uri)

    def read_file_from_uri(self, uri):
        """Reads the file from Github

        :param uri: URI of the Github raw File

        :returns: UTF-8 text with the content
        """
        logger.debug('Reading %s' % uri)
        self.__check_looks_like_uri(uri)
        try:
            req = urllib.request.Request(uri)
            req.add_header('Authorization', 'token %s' % self.token)
            r = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                raise GithubFileNotFound('File %s is not available. Check the URL to ensure it really exists' % uri)
            else:
                raise
        return r.read().decode('utf-8')