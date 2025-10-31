from threading import Thread, Lock
import time

class Listener:
    task_queue = []
    lock = Lock()
    thread = None

    @classmethod
    def _process_tasks(cls):
        while True:
            task = None
            with cls.lock:
                if cls.task_queue:
                    task = cls.task_queue.pop(0)
            if task is None:
                time.sleep(0.001)
                continue
            func, args, kwargs = task
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f'Error in listener thread: {e}')

    @classmethod
    def add_task(cls, func, *args, **kwargs):
        with cls.lock:
            cls.task_queue.append((func, args, kwargs))
        if cls.thread is None:
            cls.thread = Thread(target=cls._process_tasks, daemon=True)
            cls.thread.start()