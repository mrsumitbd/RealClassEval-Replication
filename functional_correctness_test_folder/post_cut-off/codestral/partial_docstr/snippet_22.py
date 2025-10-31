
import re
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            'technical': ['algorithm', 'implementation', 'complexity', 'density', 'detail'],
            'scientific': ['hypothesis', 'experiment', 'theory', 'data', 'analysis'],
            'fiction': ['character', 'plot', 'setting', 'dialogue', 'theme']
        }

        scores = {}
        for doc_type, _ in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, indicators)

        max_score = max(scores.values())
        doc_type = [k for k, v in scores.items() if v == max_score][0]

        return doc_type, max_score

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        total_score = 0
        for doc_type, words in indicators.items():
            score = sum(content.lower().count(word) for word in words)
            total_score += score * len(words)

        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 1
        return score / len(patterns) if patterns else 0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == 'technical':
            return 'algorithm_density'
        elif doc_type == 'scientific':
            return 'concept_complexity'
        elif doc_type == 'fiction':
            return 'implementation_detail_level'
        else:
            return 'default'

    def _calculate_algorithm_density(self, content: str) -> float:
        patterns = ['algorithm', 'pseudocode', 'flowchart', 'complexity']
        return self._detect_pattern_score(content, patterns)

    def _calculate_concept_complexity(self, content: str) -> float:
        patterns = ['hypothesis', 'theory', 'model', 'equation', 'variable']
        return self._detect_pattern_score(content, patterns)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        patterns = ['implementation', 'detail', 'step', 'procedure', 'example']
        return self._detect_pattern_score(content, patterns)
