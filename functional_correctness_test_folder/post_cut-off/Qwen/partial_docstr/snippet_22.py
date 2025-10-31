
from typing import Tuple, Dict, List
import re


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            'academic': ['research', 'literature', 'theoretical', 'hypothesis'],
            'technical': ['algorithm', 'implementation', 'code', 'software'],
            'financial': ['market', 'investment', 'profit', 'loss'],
            'legal': ['contract', 'agreement', 'legislation', 'compliance']
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {doc_type: indicators[doc_type]}) for doc_type in indicators}
        best_match = max(scores, key=scores.get)
        return best_match, scores[best_match]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            total_score += self._detect_pattern_score(content, patterns)
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            matches = re.findall(r'\b' + re.escape(pattern) +
                                 r'\b', content, re.IGNORECASE)
            score += len(matches)
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == 'academic':
            return 'paragraphs'
        elif doc_type == 'technical':
            return 'sections'
        elif doc_type == 'financial':
            return 'statements'
        elif doc_type == 'legal':
            return 'clauses'
        else:
            return 'unknown'

    def _calculate_algorithm_density(self, content: str) -> float:
        algorithm_keywords = ['algorithm', 'function', 'procedure', 'method']
        total_words = len(content.split())
        algorithm_count = sum(content.lower().count(keyword)
                              for keyword in algorithm_keywords)
        return algorithm_count / total_words if total_words > 0 else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        complex_words = ['theoretical', 'hypothesis',
                         'compliance', 'legislation', 'investment', 'market']
        total_words = len(content.split())
        complex_word_count = sum(content.lower().count(word)
                                 for word in complex_words)
        return complex_word_count / total_words if total_words > 0 else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        detail_keywords = ['implementation', 'code',
                           'software', 'library', 'framework']
        total_words = len(content.split())
        detail_count = sum(content.lower().count(keyword)
                           for keyword in detail_keywords)
        return detail_count / total_words if total_words > 0 else 0.0
