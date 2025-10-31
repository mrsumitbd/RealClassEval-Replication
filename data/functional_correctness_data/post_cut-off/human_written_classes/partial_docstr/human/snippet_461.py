from module.logger import logger
from module.base.utils import load_image, get_bbox, get_color, image_size
import os
from module.config.config import NikkeConfig
import numpy as np
import imageio

class ImageExtractor:

    def __init__(self, module, file):
        """
        Args:
            module(str):
            file(str): xxx.png or xxx.gif
        """
        self.module = module
        self.name, self.ext = os.path.splitext(file)
        self.area, self.color, self.button, self.file = ({}, {}, {}, {})
        self.load()

    def get_file(self, genre='', language='zh-cn'):
        for ext in ['.png', '.gif']:
            file = f'{self.name}.{genre}{ext}' if genre else f'{self.name}{ext}'
            file = os.path.join(NikkeConfig.ASSETS_FOLDER, 'minigame', self.module, file).replace('\\', '/')
            if os.path.exists(file):
                return file
        ext = '.png'
        file = f'{self.name}.{genre}{ext}' if genre else f'{self.name}{ext}'
        file = os.path.join(NikkeConfig.ASSETS_FOLDER, 'minigame', self.module, file).replace('\\', '/')
        return file

    def extract(self, file):
        if os.path.splitext(file)[1] == '.gif':
            bbox = None
            mean = None
            for image in imageio.mimread(file):
                image = image[:, :, :3] if len(image.shape) == 3 else image
                new_bbox, new_mean = self._extract(image, file)
                if bbox is None:
                    bbox = new_bbox
                elif bbox != new_bbox:
                    logger.warning(f'{file} has multiple different bbox, this will cause unexpected behaviour')
                if mean is None:
                    mean = new_mean
            return (bbox, mean)
        else:
            image = load_image(file)
            return self._extract(image, file)

    @staticmethod
    def _extract(image, file):
        size = image_size(image)
        if size != (720, 1280):
            logger.warning(f'{file} has wrong resolution: {size}')
        bbox = get_bbox(image)
        mean = get_color(image=image, area=bbox)
        mean = tuple(np.rint(mean).astype(int))
        return (bbox, mean)

    def load(self, language='zh-cn'):
        file = self.get_file(language=language)
        if os.path.exists(file):
            area, color = self.extract(file)
            button = area
            override = self.get_file('AREA', language=language)
            if os.path.exists(override):
                area, _ = self.extract(override)
            override = self.get_file('COLOR', language=language)
            if os.path.exists(override):
                _, color = self.extract(override)
            override = self.get_file('BUTTON', language=language)
            if os.path.exists(override):
                button, _ = self.extract(override)
            self.area[language] = area
            self.color[language] = color
            self.button[language] = button
            self.file[language] = file
        else:
            logger.attr(language, f'{self.name} not found, use zh-cn language assets')
            self.area[language] = self.area['zh-cn']
            self.color[language] = self.color['zh-cn']
            self.button[language] = self.button['zh-cn']
            self.file[language] = self.file['zh-cn']

    @property
    def expression(self):
        return '%s = Button(area=%s, color=%s, button=%s, file=%s)' % (self.name, self.area, self.color, self.button, self.file)