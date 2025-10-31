import sys
import logging

class StreamToLogger:

    def __init__(self, logger_instance, log_level=logging.INFO):
        self.logger = logger_instance
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        try:
            temp_linebuf = self.linebuf + buf
            self.linebuf = ''
            for line in temp_linebuf.splitlines(True):
                if line.endswith(('\n', '\r')):
                    self.logger.log(self.log_level, line.rstrip())
                else:
                    self.linebuf += line
        except Exception as e:
            print(f'StreamToLogger 错误: {e}', file=sys.__stderr__)

    def flush(self):
        try:
            if self.linebuf != '':
                self.logger.log(self.log_level, self.linebuf.rstrip())
            self.linebuf = ''
        except Exception as e:
            print(f'StreamToLogger Flush 错误: {e}', file=sys.__stderr__)

    def isatty(self):
        return False