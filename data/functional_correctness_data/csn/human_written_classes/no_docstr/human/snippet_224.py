from time import sleep
import multiprocessing as mp

class TextureGenerator:

    def __init__(self):
        self.queue = mp.Queue()
        self.process = mp.Process(target=self.do_work, args=(self.queue,), daemon=True)

    def do_work(self, queue):
        while True:
            if self.queue.qsize() > 60:
                sleep(0.5)
            queue.put(gen_texture(), block=False)

    def start(self):
        self.process.start()

    def stop(self):
        self.process.terminate()