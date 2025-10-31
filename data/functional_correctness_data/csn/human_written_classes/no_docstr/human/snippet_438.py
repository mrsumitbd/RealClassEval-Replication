import os
import time
import subprocess

class Notify:

    def __init__(self, msg=lambda t: 'Job finished in %.1f seconds' % t):
        self.msg = msg
        self.t0 = time.time()

    def __enter__(self):
        pass

    def notify(self, title, message):
        if os.environ.get('DISPLAY', ''):
            subprocess.call(['notify-send', title, message])
        else:
            print(title)
            print(message)

    def __exit__(self, exc_t, exc_v, tb):
        if exc_t is None:
            title = 'Success'
        else:
            title = 'Failure'
        self.notify(title, self.msg(time.time() - self.t0))