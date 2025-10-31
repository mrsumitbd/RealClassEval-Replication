import os
import threading
import json

class AsyncLogLoader:
    """异步日志加载器"""

    def __init__(self, callback):
        self.callback = callback
        self.loading = False
        self.should_stop = False

    def load_file_async(self, file_path, progress_callback=None):
        """异步加载日志文件"""
        if self.loading:
            return
        self.loading = True
        self.should_stop = False

        def load_worker():
            try:
                log_index = LogIndex()
                if not os.path.exists(file_path):
                    self.callback(log_index, '文件不存在')
                    return
                file_size = os.path.getsize(file_path)
                processed_size = 0
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = 0
                    batch_size = 1000
                    while not self.should_stop:
                        lines = []
                        for _ in range(batch_size):
                            line = f.readline()
                            if not line:
                                break
                            lines.append(line)
                            processed_size += len(line.encode('utf-8'))
                        if not lines:
                            break
                        for line in lines:
                            try:
                                log_entry = json.loads(line.strip())
                                log_index.add_entry(line_count, log_entry)
                                line_count += 1
                            except json.JSONDecodeError:
                                continue
                        if progress_callback:
                            progress = min(100, processed_size / file_size * 100)
                            progress_callback(progress, line_count)
                if not self.should_stop:
                    self.callback(log_index, None)
            except Exception as e:
                self.callback(None, str(e))
            finally:
                self.loading = False
        thread = threading.Thread(target=load_worker)
        thread.daemon = True
        thread.start()

    def stop_loading(self):
        """停止加载"""
        self.should_stop = True
        self.loading = False