from PySide6.QtCore import QThread, Signal, QObject

class DiscordRPC:

    def __init__(self, client_id='1392812529259909161'):
        self.client_id = client_id
        self.thread = None
        self.worker = None

    def start(self):
        if self.is_running():
            return
        self.thread = QThread()
        self.worker = RPCWorker(self.client_id)
        self.worker.moveToThread(self.thread)
        self.worker.error.connect(self.on_error)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def stop(self):
        if self.worker:
            self.worker.stop()
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        self.thread = None
        self.worker = None

    def on_error(self, error_message):
        print(f'Discord RPC Error: {error_message}')

    def is_running(self):
        return self.thread is not None and self.thread.isRunning()