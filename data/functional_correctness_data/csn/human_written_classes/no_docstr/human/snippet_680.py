import logging

class StderrWriter:

    def write(self, message):
        message = message.strip()
        if message:
            logging.error(message)

    def flush(self):
        pass