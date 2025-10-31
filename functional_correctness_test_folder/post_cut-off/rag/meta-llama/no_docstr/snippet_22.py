
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
            'technical_document': ['algorithm', 'implementation', 'code', 'programming'],
            'research_paper': ['research', 'study', 'analysis', 'findings'],
            'blog_post': ['blog', 'article', 'opinion', 'news']
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {indicator: patterns for indicator, patterns in indicators.items() if indicator == doc_type}) for doc_type in indicators}
        doc_type = max(scores, key=scores.get)
        return doc_type, scores[doc_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate weighted semantic indicator scores"""
        scores = [self._detect_pattern_score(
            content, patterns) for patterns in indicators.values()]
        return np.mean(scores)

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """Detect semantic pattern matching scores"""
        matches = sum(1 for pattern in patterns if re.search(
            pattern, content, re.IGNORECASE))
        return matches / len(patterns)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        """
        if doc_type == 'technical_document':
            algorithm_density = self._calculate_algorithm_density(content)
            if algorithm_density > 0.5:
                return 'code_block_segmentation'
            else:
                return 'header_segmentation'
        elif doc_type == 'research_paper':
            concept_complexity = self._calculate_concept_complexity(content)
            if concept_complexity > 0.7:
                return 'section_segmentation'
            else:
                return 'paragraph_segmentation'
        else:
            return 'default_segmentation'

    def _calculate_algorithm_density(self, content: str) -> float:
        """Calculate algorithm content density"""
        code_keywords = ['if', 'else', 'for', 'while', 'function', 'class']
        words = re.findall(r'\b\w+\b', content.lower())
        code_word_count = sum(1 for word in words if word in code_keywords)
        return code_word_count / len(words)

    def _calculate_concept_complexity(self, content: str) -> float:
        """Calculate concept complexity"""
        complex_words = ['however', 'nevertheless',
                         'thus', 'therefore', 'consequently']
        words = re.findall(r'\b\w+\b', content.lower())
        complex_word_count = sum(1 for word in words if word in complex_words)
        return complex_word_count / len(words)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """Calculate implementation detail level"""
        implementation_keywords = ['implementation',
                                   'code', 'programming', 'algorithm']
        words = re.findall(r'\b\w+\b', content.lower())
        implementation_word_count = sum(
            1 for word in words if word in implementation_keywords)
        return implementation_word_count / len(words)
