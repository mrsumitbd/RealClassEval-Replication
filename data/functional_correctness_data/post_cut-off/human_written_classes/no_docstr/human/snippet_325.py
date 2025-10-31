import os
from module.config.config import NikkeConfig
from module.logger import logger

class ModuleExtractor:

    def __init__(self, name):
        self.name = name
        self.folder = os.path.join(NikkeConfig.ASSETS_FOLDER, 'event', name)
        '\n            os.path.join(MODULE_FOLDER, self.name)\n            ./module\\event_1\n            \n            self.folder\n            ./assets\\event\\event_1\n        '

    @staticmethod
    def split(file):
        name, ext = os.path.splitext(file)
        name, sub = os.path.splitext(name)
        return (name, sub, ext)

    def is_base_image(self, file):
        _, sub, _ = self.split(file)
        return sub == ''

    @property
    def expression(self):
        exp = []
        for file in os.listdir(self.folder):
            if file[0].isdigit():
                continue
            if file.startswith('TEMPLATE_'):
                exp.append(TemplateExtractor(module=self.name, file=file).expression)
                continue
            if self.is_base_image(file):
                exp.append(ImageExtractor(module=self.name, file=file).expression)
                continue
        logger.info('Module: %s(%s)' % (self.name, len(exp)))
        exp = IMPORT_EXP + exp
        return exp

    def write(self):
        folder = os.path.join(MODULE_FOLDER, 'event', self.name)
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(os.path.join(folder, BUTTON_FILE), 'w', newline='') as f:
            for text in self.expression:
                f.write(text + '\n')