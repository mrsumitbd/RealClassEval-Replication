class TqdmLoggingHandler:

    def __init__(self):
        pass

    def write(self, msg):
        logger.info(msg.strip())

    def flush(self):
        pass