
import re
from typing import Tuple, Dict, List


class DocumentAnalyzer:

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        indicators = {
            'algorithm': ['algorithm', 'pseudocode', 'steps', 'procedure', 'flowchart'],
            'concept': ['concept', 'definition', 'explanation', 'overview', 'introduction'],
            'implementation': ['implementation', 'code', 'example', 'snippet', 'demo']
        }

        algorithm_score = self._calculate_weighted_score(
            content, {'algorithm': indicators['algorithm']})
        concept_score = self._calculate_weighted_score(
            content, {'concept': indicators['concept']})
        implementation_score = self._calculate_weighted_score(
            content, {'implementation': indicators['implementation']})

        max_score = max(algorithm_score, concept_score, implementation_score)

        if max_score == algorithm_score:
            return 'algorithm', algorithm_score
        elif max_score == concept_score:
            return 'concept', concept_score
        else:
            return 'implementation', implementation_score

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        total_score = 0.0
        for category, patterns in indicators.items():
            score = self._detect_pattern_score(content, patterns)
            total_score += score
        return total_score / len(indicators)

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        content_lower = content.lower()
        score = 0.0
        for pattern in patterns:
            if pattern in content_lower:
                score += 1.0
        return score / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        if doc_type == 'algorithm':
            density = self._calculate_algorithm_density(content)
            if density > 0.5:
                return 'high_density'
            else:
                return 'low_density'
        elif doc_type == 'concept':
            complexity = self._calculate_concept_complexity(content)
            if complexity > 0.5:
                return 'high_complexity'
            else:
                return 'low_complexity'
        elif doc_type == 'implementation':
            detail_level = self._calculate_implementation_detail_level(content)
            if detail_level > 0.5:
                return 'high_detail'
            else:
                return 'low_detail'
        else:
            return 'unknown'

    def _calculate_algorithm_density(self, content: str) -> float:
        patterns = ['algorithm', 'pseudocode',
                    'steps', 'procedure', 'flowchart']
        return self._detect_pattern_score(content, patterns)

    def _calculate_concept_complexity(self, content: str) -> float:
        patterns = ['concept', 'definition',
                    'explanation', 'overview', 'introduction']
        return self._detect_pattern_score(content, patterns)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        patterns = ['implementation', 'code', 'example', 'snippet', 'demo']
        return self._detect_pattern_score(content, patterns)
