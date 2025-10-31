import re
import sys
from pathlib import Path
import hashlib
import stat
import time
import subprocess
import os
import httpx
import platform

class Tunnel:

    def __init__(self, remote_host: str, remote_port: int, local_host: str, local_port: int, share_token: str, http: bool, share_server_tls_certificate: str | None):
        self.proc = None
        self.url = None
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_host = local_host
        self.local_port = local_port
        self.share_token = share_token
        self.http = http
        self.share_server_tls_certificate = share_server_tls_certificate

    @staticmethod
    def download_binary():
        if not Path(BINARY_PATH).exists():
            Path(BINARY_FOLDER).mkdir(parents=True, exist_ok=True)
            resp = httpx.get(BINARY_URL, timeout=30)
            if resp.status_code == 403:
                raise OSError(f'Cannot set up a share link as this platform is incompatible. Please create a GitHub issue with information about your platform: {platform.uname()}')
            resp.raise_for_status()
            with open(BINARY_PATH, 'wb') as file:
                file.write(resp.content)
            st = os.stat(BINARY_PATH)
            os.chmod(BINARY_PATH, st.st_mode | stat.S_IEXEC)
            if BINARY_URL in CHECKSUMS:
                sha = hashlib.sha256()
                with open(BINARY_PATH, 'rb') as f:
                    for chunk in iter(lambda: f.read(CHUNK_SIZE * sha.block_size), b''):
                        sha.update(chunk)
                calculated_hash = sha.hexdigest()
                if calculated_hash != CHECKSUMS[BINARY_URL]:
                    raise ValueError('Checksum mismatch for frpc binary')

    def start_tunnel(self) -> str:
        self.download_binary()
        self.url = self._start_tunnel(BINARY_PATH)
        return self.url

    def kill(self):
        if self.proc is not None:
            print(f'Killing tunnel {self.local_host}:{self.local_port} <> {self.url}')
            self.proc.terminate()
            self.proc = None

    def _start_tunnel(self, binary: str) -> str:
        command = [binary, 'http', '-n', self.share_token, '-l', str(self.local_port), '-i', self.local_host, '--uc', '--sd', 'random', '--ue', '--server_addr', f'{self.remote_host}:{self.remote_port}', '--disable_log_color']
        if self.share_server_tls_certificate is not None:
            command.extend(['--tls_enable', '--tls_trusted_ca_file', self.share_server_tls_certificate])
        if not self.http:
            command.append('--tls_enable')
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        return self._read_url_from_tunnel_stream()

    def _read_url_from_tunnel_stream(self) -> str:
        start_timestamp = time.time()
        log = []
        url = ''

        def _raise_tunnel_error():
            log_text = '\n'.join(log)
            print(log_text, file=sys.stderr)
            raise ValueError(f'{TUNNEL_ERROR_MESSAGE}\n{log_text}')
        while url == '':
            if time.time() - start_timestamp >= TUNNEL_TIMEOUT_SECONDS:
                _raise_tunnel_error()
            assert self.proc is not None
            if self.proc.stdout is None:
                continue
            line = self.proc.stdout.readline()
            line = line.decode('utf-8')
            if line == '':
                continue
            log.append(line.strip())
            if 'start proxy success' in line:
                result = re.search('start proxy success: (.+)\n', line)
                if result is None:
                    _raise_tunnel_error()
                else:
                    url = result.group(1)
            elif 'login to server failed' in line:
                _raise_tunnel_error()
        if self.http:
            url = url.replace('https://', 'http://')
        return url