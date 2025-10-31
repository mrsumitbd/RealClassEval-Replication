import logging

class StdoutWriter:

    def write(self, message):
        message = message.strip()
        if message:
            logging.info(message)

    def flush(self):
        pass