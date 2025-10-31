from PIL import Image
from pdfconduit.watermark.modify.draw import WatermarkDraw
from pathlib import Path
from tempfile import TemporaryDirectory
from pdfconduit.watermark.modify.canvas import CanvasImg, CanvasObjects
from typing import List, Optional, Union
from pdfconduit.transform import Merge2
import os

class IMG2PDF:

    def __init__(self, images: Union[str, List[str]], output: Optional[str]=None, tempdir: Optional[TemporaryDirectory]=None):
        """Convert each image into a PDF page and merge all pages to one PDF file"""
        self.images = images if isinstance(images, list) else [images]
        self.output = output
        self._tempdir = tempdir or TemporaryDirectory()

    def convert(self, cleanup_temp: bool=True) -> str:
        pdfs = [self._convert_image_to_pdf(image) for image in self.images]
        merged = Merge2(pdfs, output=self.output).merge()
        return merged

    def cleanup(self) -> None:
        self._tempdir.cleanup()

    def _convert_image_to_pdf(self, image: str) -> str:
        with Image.open(image) as im:
            width, height = im.size
            co = CanvasObjects()
            co.add(CanvasImg(image, 1.0, w=width, h=height, mask=None))
            return WatermarkDraw(co, tempdir=self._tempdir.name, pagesize=(width, height)).write(os.path.join(self._tempdir.name, os.path.basename(image.replace(Path(image).suffix, '.pdf'))))