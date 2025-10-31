import os
from bcbio.distributed.transaction import file_transaction
from bcbio.provenance import do
from bcbio import utils
import re

class RegularServer:
    """Files stored in FTP/http that can be downloaded by wget
    """

    @classmethod
    def _parse_url(self, fn):
        regex = re.compile('^(?:http|ftp)s?://.*(.fastq.gz)[^/]*|^(?:http|ftp)s?://.*(.fastq)[^/]*|^(?:http|ftp)s?://.*(.bam)[^/]*', re.IGNORECASE)
        return regex.match(fn)

    @classmethod
    def check_resource(self, resource):
        if self._parse_url(resource):
            return True

    @classmethod
    def download(self, filename, input_dir, dl_dir=None):
        match = self._parse_url(filename)
        file_info = os.path.basename(filename)
        ext = file_info.find(match.group(1))
        name = file_info[:ext]
        if not dl_dir:
            dl_dir = os.path.join(input_dir, name)
            utils.safe_makedir(dl_dir)
        fixed_name = '%s%s' % (name, match.group(1))
        out_file = os.path.join(dl_dir, fixed_name)
        if not utils.file_exists(out_file):
            with file_transaction({}, out_file) as tx_out_file:
                cmd = 'wget -O {tx_out_file} {filename}'
                do.run(cmd.format(**locals()), 'Download %s' % out_file)
        return out_file