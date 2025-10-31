import time
from module.base.utils import crop, float2str
import numpy as np
from typing import TYPE_CHECKING, Dict, List
from module.ocr.models import OCR_MODEL
from module.logger import logger
from module.ocr.models import OCR_MODEL
import cv2
from module.base.button import Button

class Ocr:
    SHOW_REVISE_WARNING = False

    def __init__(self, buttons, lang='ch', model_type='mobile', interval=0, name=None):
        """
        Args:
            buttons (Button, tuple, list[Button], list[tuple]): OCR area.
            lang (str): 'ch' , 'en' or 'num'.
            model_type (str): 'mobile' or 'server'
            name (str):
        """
        self.name = str(buttons) if isinstance(buttons, Button) else name
        self._buttons = buttons
        self.model_type = model_type
        self.lang = lang
        self.interval = interval

    @property
    def paddleocr(self) -> 'NIKKEOcr':
        return OCR_MODEL.get_model_by(lang=self.lang, model_type=self.model_type, interval=self.interval)

    @property
    def buttons(self):
        buttons = self._buttons
        buttons = buttons if isinstance(buttons, list) else [buttons]
        buttons = [button.area if isinstance(button, Button) else button for button in buttons]
        return buttons

    @buttons.setter
    def buttons(self, value):
        self._buttons = value

    def pre_process(self, image):
        """
        Args:
            image (np.ndarray): Shape (height, width, channel)

        Returns:
            np.ndarray: Shape (width, height)
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        binary_colored = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        return binary_colored.astype(np.uint8)

    def after_process(self, result):
        """
        Args:
            result (str): OCR result string

        Returns:
            str:
        """
        return result

    def ocr(self, image, direct_ocr=False, threshold: float=0.51, show_log=True):
        """
        Args:
            image (np.ndarray, list[np.ndarray]):
            direct_ocr (bool): True to skip cropping.

        Returns:
            list[str] or str
        """
        start_time = time.time()
        images_to_ocr = []
        if direct_ocr:
            images_to_ocr = [image]
        else:
            images_to_ocr = [crop(image, area) for area in self.buttons]
        result = self.paddleocr.predict(images_to_ocr)
        processed_result = self._process_ocr_result(result, threshold)
        processed_result['text'] = self.after_process(processed_result['text'])
        if show_log:
            logger.attr(name='%s %ss' % (self.name, float2str(time.time() - start_time)), text=str(processed_result['text'].replace('\n', ' ')))
        return processed_result

    def _process_ocr_result(self, result: List[dict], threshold: float) -> Dict:
        """
        处理 Paddlex OCR dict 格式的识别结果，仅使用 rec_texts/rec_scores/rec_boxes。

        Args:
            result: OCR 原始结果，每项为 dict，需包含 'rec_texts', 'rec_scores', 'rec_boxes'
            threshold: 置信度阈值

        Returns:
            Dict: {
                'text': str,               # 合并后的文本
                'details': List[dict],     # 每行的详细信息
                'stats': {
                    'total_lines': int,    # 有效行数
                    'total_chars': int,    # 总字符数（不含空格和换行）
                    'avg_confidence': float,# 平均置信度
                    'confidence_threshold': float,
                }
            }
        """
        text_lines = []
        details = []
        total_conf = 0.0
        valid_lines = 0
        if not result:
            return {'text': '', 'details': [], 'stats': {'total_lines': 0, 'total_chars': 0, 'avg_confidence': 0.0, 'confidence_threshold': threshold}}
        for page in result:
            rec_texts = page.get('rec_texts', [])
            rec_scores = page.get('rec_scores', [])
            rec_boxes = page.get('rec_boxes', [])
            for idx, (txt, score) in enumerate(zip(rec_texts, rec_scores)):
                text = txt.strip()
                confidence = float(score)
                if confidence < threshold or not text:
                    continue
                bbox = rec_boxes[idx] if idx < len(rec_boxes) else []
                valid_lines += 1
                total_conf += confidence
                text_lines.append(text)
                details.append({'line_number': valid_lines, 'text': text, 'confidence': confidence, 'bbox': bbox, 'char_count': len(text)})
        combined_text = ''.join(text_lines)
        avg_conf = total_conf / valid_lines if valid_lines > 0 else 0.0
        total_chars = len(combined_text.replace('\n', '').replace(' ', ''))
        return {'text': combined_text, 'details': details, 'stats': {'total_lines': valid_lines, 'total_chars': total_chars, 'avg_confidence': avg_conf, 'confidence_threshold': threshold}}