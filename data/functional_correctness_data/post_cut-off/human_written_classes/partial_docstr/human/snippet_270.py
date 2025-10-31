import datetime

class LoggerWriter:
    """
    標準出力をラップしてログファイルにも書き込むクラス
    """

    def __init__(self, original_stream, log_file):
        self.original_stream = original_stream
        self.log_file = log_file

    def write(self, text):
        self.original_stream.write(text)
        if self.log_file and (not self.log_file.closed):
            if not text.strip():
                return
            is_progress_bar = False
            if '\r' in text or ('%' in text and ('|' in text or '/' in text)):
                is_progress_bar = True
            timestamp = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            if is_progress_bar:
                global _last_progress_percent, _progress_log_interval
                import re
                progress_match = re.search('(\\d+)%', text)
                if progress_match:
                    percent = int(progress_match.group(1))
                    should_log = _last_progress_percent is None or percent == 0 or percent == 100 or (_last_progress_percent is not None and abs(percent - _last_progress_percent) >= _progress_log_interval)
                    if should_log:
                        _last_progress_percent = percent
                        count_match = re.search('(\\d+)/(\\d+)', text)
                        if count_match:
                            current, total = count_match.groups()
                            self.log_file.write(f'{timestamp} [PROGRESS] {percent}% ({current}/{total})\n')
                        else:
                            self.log_file.write(f'{timestamp} [PROGRESS] {percent}%\n')
                else:
                    progress_text = text.strip().replace('\r', '').split('\n')[-1][:50]
                    self.log_file.write(f'{timestamp} [PROGRESS] {progress_text}\n')
            else:
                for line in text.split('\n'):
                    if line.strip():
                        self.log_file.write(f'{timestamp} {line}\n')
            self.log_file.flush()

    def flush(self):
        self.original_stream.flush()
        if self.log_file and (not self.log_file.closed):
            self.log_file.flush()

    def fileno(self):
        return self.original_stream.fileno()

    def isatty(self):
        return self.original_stream.isatty()