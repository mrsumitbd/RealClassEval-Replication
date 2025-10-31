import socket
import threading
import smtplib

class EmailBase:
    transferSize = 0
    progress = 0

    def data(self, msg):
        self.transferSize = len(msg)
        code, resp = smtplib.SMTP.data(self, msg)
        self.progress = 0
        return (code, resp)

    def send(self, strg):
        """Send 'strg' to the server."""
        log.debug_no_auth('send: {}'.format(strg[:300]), stacklevel=2)
        if hasattr(self, 'sock') and self.sock:
            try:
                if self.transferSize:
                    lock = threading.Lock()
                    lock.acquire()
                    self.transferSize = len(strg)
                    lock.release()
                    for i in range(0, self.transferSize, CHUNKSIZE):
                        if isinstance(strg, bytes):
                            self.sock.send(strg[i:i + CHUNKSIZE])
                        else:
                            self.sock.send(strg[i:i + CHUNKSIZE].encode('utf-8'))
                        lock.acquire()
                        self.progress = i
                        lock.release()
                else:
                    self.sock.sendall(strg.encode('utf-8'))
            except socket.error:
                self.close()
                raise smtplib.SMTPServerDisconnected('Server not connected')
        else:
            raise smtplib.SMTPServerDisconnected('please run connect() first')

    @classmethod
    def _print_debug(cls, *args):
        log.debug(args)

    def getTransferStatus(self):
        if self.transferSize:
            lock2 = threading.Lock()
            lock2.acquire()
            value = int(float(self.progress) / float(self.transferSize) * 100)
            lock2.release()
            return value / 100
        else:
            return 1