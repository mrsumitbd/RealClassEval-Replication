
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            'technical': ['algorithm', 'data structure', 'complexity'],
            'non-technical': ['management', 'business', 'marketing']
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {indicator: indicators[indicator] for indicator in indicators if indicator == doc_type or doc_type == 'all'}) for doc_type in indicators}
        doc_type = max(scores, key=scores.get)
        return doc_type, scores[doc_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        score = 0.0
        for indicator, keywords in indicators.items():
            for keyword in keywords:
                score += content.lower().count(keyword.lower())
        return score / len(content.split()) if content else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        score = 0.0
        for pattern in patterns:
            score += content.lower().count(pattern.lower())
        return score / len(content.split()) if content else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == 'technical':
            algorithm_density = self._calculate_algorithm_density(content)
            if algorithm_density > 0.5:
                return 'section-based'
            else:
                return 'paragraph-based'
        else:
            concept_complexity = self._calculate_concept_complexity(content)
            if concept_complexity > 0.7:
                return 'section-based'
            else:
                return 'paragraph-based'

    def _calculate_algorithm_density(self, content: str) -> float:
        patterns = ['if', 'else', 'for', 'while', 'function']
        return self._detect_pattern_score(content, patterns)

    def _calculate_concept_complexity(self, content: str) -> float:
        complex_words = ['however', 'in addition', 'nevertheless', 'thus']
        return self._detect_pattern_score(content, complex_words)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        implementation_keywords = ['code', 'implementation', 'example']
        return self._calculate_weighted_score(content, {'implementation': implementation_keywords})
