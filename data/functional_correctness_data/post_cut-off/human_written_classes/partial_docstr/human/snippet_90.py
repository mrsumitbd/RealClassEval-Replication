from typing import Union
from loguru import logger
import time
from io import BytesIO
import PIL
import numpy as np
import base64
from src.engine_utils.directory_info import DirectoryInfo

class ImageUtils:

    @staticmethod
    def format_image(image: Union[str, np.ndarray]):
        if isinstance(image, np.ndarray):
            return ImageUtils.numpy2base64(image)
        return image

    @staticmethod
    def numpy2base64(video_frame, format='JPEG'):
        image = PIL.Image.fromarray(np.squeeze(video_frame)[..., ::-1])
        buffered = BytesIO()
        image.save(buffered, format=format)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        data_url = f'data:image/{format.lower()};base64,{base64_image}'
        dump_image = False
        if dump_image:
            from engine_utils.directory_info import DirectoryInfo
            ImageUtils.save_base64_image(base64_image, f'{DirectoryInfo.get_project_dir()}/temp/{time.localtime().tm_min}_{time.localtime().tm_sec}.jpg')
        return data_url

    @staticmethod
    def save_base64_image(base64_data, output_path):
        """
        将 Base64 编码的图片保存为本地文件。

        :param base64_data: Base64 编码的图片字符串（不包括头部信息）
        :param output_path: 保存图片的本地路径（包含文件名和扩展名）
        """
        try:
            if ',' in base64_data:
                _, base64_data = base64_data.split(',', 1)
            image_data = base64.b64decode(base64_data)
            with open(output_path, 'wb') as f:
                f.write(image_data)
            logger.debug(f'图片已成功保存至 {output_path}')
        except Exception as e:
            logger.debug(f'保存图片时出错: {e}')