
from typing import Dict, List, Tuple
import re
from collections import Counter
import numpy as np


class DocumentAnalyzer:
    """Enhanced document analyzer using semantic content analysis instead of mechanical structure detection"""

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        """
        indicators = {
            'technical_document': ['algorithm', 'implementation', 'code'],
            'research_paper': ['study', 'research', 'methodology'],
            'blog_post': ['blog', 'article', 'opinion']
        }
        scores = {doc_type: self._calculate_weighted_score(content, {indicator: patterns for indicator, patterns in indicators.items(
        ) if indicator.startswith(doc_type)}) for doc_type in set([indicator.split('_')[0] for indicator in indicators.keys()])}
        doc_type = max(scores, key=scores.get)
        return doc_type, scores[doc_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate weighted semantic indicator scores"""
        scores = [self._detect_pattern_score(
            content, patterns) for patterns in indicators.values()]
        return np.mean(scores)

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """Detect semantic pattern matching scores"""
        matches = sum([len(re.findall(pattern, content, re.IGNORECASE))
                      for pattern in patterns])
        return matches / len(patterns) if patterns else 0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        """
        algorithm_density = self._calculate_algorithm_density(content)
        concept_complexity = self._calculate_concept_complexity(content)
        implementation_detail_level = self._calculate_implementation_detail_level(
            content)
        if doc_type == 'technical_document':
            if algorithm_density > 0.5 and concept_complexity > 0.5:
                return 'detailed_segmentation'
            else:
                return 'coarse_segmentation'
        elif doc_type == 'research_paper':
            if implementation_detail_level > 0.5:
                return 'fine_grained_segmentation'
            else:
                return 'section_based_segmentation'
        else:
            return 'default_segmentation'

    def _calculate_algorithm_density(self, content: str) -> float:
        """Calculate algorithm content density"""
        algorithm_related_words = ['algorithm', 'data structure', 'complexity']
        word_count = len(re.findall(r'\b\w+\b', content))
        algorithm_word_count = sum(
            [len(re.findall(word, content, re.IGNORECASE)) for word in algorithm_related_words])
        return algorithm_word_count / word_count if word_count > 0 else 0

    def _calculate_concept_complexity(self, content: str) -> float:
        """Calculate concept complexity"""
        complex_words = [word for word, count in Counter(
            re.findall(r'\b\w+\b', content)).items() if count > 1]
        return len(complex_words) / len(re.findall(r'\b\w+\b', content)) if re.findall(r'\b\w+\b', content) else 0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """Calculate implementation detail level"""
        implementation_related_words = ['implementation', 'code', 'example']
        word_count = len(re.findall(r'\b\w+\b', content))
        implementation_word_count = sum([len(re.findall(
            word, content, re.IGNORECASE)) for word in implementation_related_words])
        return implementation_word_count / word_count if word_count > 0 else 0
