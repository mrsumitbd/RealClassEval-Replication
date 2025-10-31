from typing import Any, Dict, List
from functools import cached_property
from difflib import SequenceMatcher
import random
from pathlib import Path
import json
from module.base.utils import remove_punctuation

class Dialogue:

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self._raw_data = None

    @property
    def raw_data(self) -> Dict[str, Any]:
        """加载原始JSON数据"""
        if self._raw_data is None:
            if not self.file_path.exists():
                print(f'文件不存在: {self.file_path}')
                self._raw_data = {}
                return self._raw_data
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self._raw_data = json.load(f)
            except json.JSONDecodeError:
                self._raw_data = {}
            except Exception:
                self._raw_data = {}
        return self._raw_data

    @cached_property
    def dialogue_data(self) -> Dict[str, Any]:
        """处理后的数据（仅处理角色名和问题，保留答案原始格式）"""

        def process_data(obj: Any) -> Any:
            """递归处理数据结构"""
            if isinstance(obj, dict):
                new_dict = {}
                for key, value in obj.items():
                    cleaned_key = remove_punctuation(key) if isinstance(key, str) else key
                    new_dict[cleaned_key] = process_data(value)
                return new_dict
            elif isinstance(obj, list):
                return [process_data(item) for item in obj]
            elif isinstance(obj, str):
                return obj
            else:
                return obj
        return process_data(self.raw_data)

    def get_answer_list(self, character: str, correct: bool) -> List[str]:
        """
        获取指定角色的所有答案
        """
        cleaned_character = remove_punctuation(character)
        character_data = self.dialogue_data.get(cleaned_character)
        if not character_data:
            return []
        answers = []
        for qa in character_data:
            answer_dict = qa.get('answer', {})
            if correct:
                correct_answer = answer_dict.get('true')
                if correct_answer:
                    if isinstance(correct_answer, list):
                        answers.extend(correct_answer)
                    else:
                        answers.append(correct_answer)
            else:
                wrong_answer = answer_dict.get('false')
                if wrong_answer:
                    if isinstance(wrong_answer, list):
                        answers.extend(wrong_answer)
                    else:
                        answers.append(wrong_answer)
        return answers

    @staticmethod
    def similarity_difflib(str1: str, str2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1, str2).ratio()

    def get_answer(self, character: str, answer_list: List[str]) -> str:
        """
        返回正确答案，AI写的
        """
        if not answer_list:
            return ''
        correct_answers = self.get_answer_list(character, True)
        wrong_answers = self.get_answer_list(character, False)
        for candidate in answer_list:
            if candidate in correct_answers:
                return candidate
        for candidate in answer_list:
            if candidate in wrong_answers:
                other_answers = [a for a in answer_list if a != candidate and a not in wrong_answers]
                if other_answers:
                    return random.choice(other_answers)
        candidate_scores = []
        for candidate in answer_list:
            max_correct_similarity = max((self.similarity_difflib(candidate, correct_answer) for correct_answer in correct_answers), default=0.0)
            max_wrong_similarity = max((self.similarity_difflib(candidate, wrong_answer) for wrong_answer in wrong_answers), default=0.0)
            confidence_score = max_correct_similarity - 0.5 * max_wrong_similarity
            candidate_scores.append((candidate, confidence_score))
        candidate_scores.sort(key=lambda x: x[1], reverse=True)
        if candidate_scores:
            best_candidate, best_score = candidate_scores[0]
            if best_score > 0.5:
                return best_candidate
        return random.choice(answer_list)