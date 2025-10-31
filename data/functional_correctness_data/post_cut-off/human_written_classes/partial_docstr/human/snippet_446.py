import socket
import time
import json
import base64

class ZhidaClient:

    def __init__(self, host='192.168.1.47', port=5792, timeout=10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        """建立 TCP 连接，并设置超时用于后续 recv/send。"""
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        self.sock.settimeout(self.timeout)

    def close(self):
        """关闭连接。"""
        if self.sock:
            self.sock.close()
            self.sock = None

    def _send_command(self, cmd: dict) -> dict:
        """
        发送一条命令，接收 raw bytes，直到能成功 json.loads。
        """
        if not self.sock:
            raise ConnectionError('Not connected')
        payload = json.dumps(cmd, ensure_ascii=False).encode('utf-8')
        self.sock.sendall(payload)
        buffer = bytearray()
        start = time.time()
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer.extend(chunk)
                text = buffer.decode('utf-8', errors='strict')
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
            except socket.timeout:
                raise TimeoutError('recv() timed out after {:.1f}s'.format(self.timeout))
            if time.time() - start > self.timeout * 2:
                raise TimeoutError('No complete JSON received after {:.1f}s'.format(time.time() - start))
        raise ConnectionError('Connection closed before JSON could be parsed')

    @property
    def status(self) -> dict:
        return self._send_command({'command': 'getstatus'})['result']

    def get_methods(self) -> dict:
        return self._send_command({'command': 'getmethods'})

    def start(self, text) -> dict:
        b64 = base64.b64encode(text.encode('utf-8')).decode('ascii')
        return self._send_command({'command': 'start', 'message': b64})

    def abort(self) -> dict:
        return self._send_command({'command': 'abort'})