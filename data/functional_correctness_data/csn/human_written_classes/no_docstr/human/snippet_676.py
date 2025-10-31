from ocrd_utils import initLogging, getLogger, getLevelName

class LogCtx:

    def __init__(self, name):
        self.name = name

    def log(self, lvl, *args, **kwargs):
        logger = getLogger(self.name)
        logger.log(getLevelName(lvl), *args, **kwargs)