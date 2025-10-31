import numpy as np

class OcrModel:

    def __init__(self):
        self._paddle_cache = {}
        self._paddle_num_cache = {}

    def paddle(self, model_type, interval):
        if model_type not in self._paddle_cache:
            from module.ocr.nikke_ocr import NIKKEOcr
            self._paddle_cache[model_type] = NIKKEOcr(lang='ch', model_type=model_type, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, interval=interval)
        return self._paddle_cache[model_type]

    def paddle_num(self, model_type, interval):
        if model_type not in self._paddle_num_cache:
            from module.ocr.nikke_ocr import NIKKEOcr
            self._paddle_num_cache[model_type] = NIKKEOcr(lang='en', model_type=model_type, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, text_det_thresh=0.1, text_det_unclip_ratio=6.0, interval=interval)
        return self._paddle_num_cache[model_type]

    def get_model_by(self, lang='ch', model_type='mobile', interval=0):
        if lang == 'ch':
            return self.paddle(model_type=model_type, interval=interval)
        elif lang in ('en', 'num'):
            return self.paddle_num(model_type=model_type, interval=interval)
        else:
            raise ValueError(f'Unsupported lang: {lang}')

    def get_location(self, text, result, threshold=0.7):
        """
        获取目标文本在 OCR 结果中的中心坐标

        Args:
            text: 要查找的目标文本
            result: _process_ocr_result 返回的结果字典
            threshold: 匹配相似度阈值 (0~1)

        Returns:
            tuple: (x, y) 中心坐标，未找到返回 None
        """
        if not result or not result.get('details'):
            return None
        text_bbox_map = {item['text']: item['bbox'] for item in result['details']}
        all_texts = list(text_bbox_map.keys())
        ratio, matched_text = self.get_similarity(all_texts, text)
        if not (ratio >= threshold and matched_text in text_bbox_map):
            return None
        raw_bbox = text_bbox_map[matched_text]
        if raw_bbox is None:
            return None
        bbox = np.array(raw_bbox)
        if bbox.ndim == 2 and bbox.shape == (4, 2):
            ul = bbox[0]
            br = bbox[2]
        elif bbox.ndim == 1 and bbox.size == 4:
            ul = bbox[:2]
            br = bbox[2:4]
        else:
            return None
        x = (int(ul[0]) + int(br[0])) / 2
        y = (int(ul[1]) + int(br[1])) / 2
        return (x, y)

    def get_similarity(self, texts, target, threshold=0.49):
        """计算文本相似度

        Args:
            texts: 候选文本列表
            target: 目标文本
            threshold: 相似度阈值

        Returns:
            tuple: (相似度, 最匹配的文本)
        """
        import difflib
        clean_target = target.strip('_')
        max_ratio = 0
        most_matched = ''
        for text in texts:
            if '_' in target and clean_target == text:
                return (1.0, text)
            ratio = difflib.SequenceMatcher(None, text, target).ratio()
            if ratio > max_ratio:
                max_ratio = ratio
                most_matched = text
        return (max_ratio, most_matched) if max_ratio >= threshold else (0, '')