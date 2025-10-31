
import re
from typing import Tuple, Dict, List
from collections import defaultdict


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = {
            'technical_manual': ['procedure', 'step', 'installation', 'maintenance', 'troubleshooting'],
            'scientific_paper': ['abstract', 'introduction', 'methodology', 'results', 'conclusion'],
            'user_guide': ['quick start', 'tutorial', 'how to', 'guide', 'manual'],
            'api_documentation': ['endpoint', 'request', 'response', 'parameter', 'authentication']
        }

        scores = {doc_type: self._calculate_weighted_score(
            content, {doc_type: indicators[doc_type]}) for doc_type in indicators}
        best_match = max(scores.items(), key=lambda x: x[1])
        return best_match[0], best_match[1]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content, patterns)
            total_score += pattern_score
        return total_score / len(indicators) if indicators else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        content_lower = content.lower()
        pattern_count = sum(
            1 for pattern in patterns if pattern.lower() in content_lower)
        return pattern_count / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        algorithm_density = self._calculate_algorithm_density(content)
        concept_complexity = self._calculate_concept_complexity(content)
        implementation_detail_level = self._calculate_implementation_detail_level(
            content)

        if doc_type == 'technical_manual':
            if algorithm_density > 0.5 and concept_complexity > 0.5:
                return 'algorithm_centric'
            elif implementation_detail_level > 0.5:
                return 'step_by_step'
            else:
                return 'section_based'
        elif doc_type == 'scientific_paper':
            if concept_complexity > 0.5:
                return 'concept_centric'
            else:
                return 'section_based'
        elif doc_type == 'user_guide':
            if implementation_detail_level > 0.5:
                return 'step_by_step'
            else:
                return 'section_based'
        elif doc_type == 'api_documentation':
            if algorithm_density > 0.5:
                return 'endpoint_centric'
            else:
                return 'section_based'
        else:
            return 'section_based'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_keywords = ['algorithm', 'function',
                              'method', 'procedure', 'pseudocode', 'code block']
        content_lower = content.lower()
        keyword_count = sum(
            1 for keyword in algorithm_keywords if keyword.lower() in content_lower)
        word_count = len(re.findall(r'\w+', content))
        return keyword_count / word_count if word_count > 0 else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        concept_keywords = ['concept', 'theory',
                            'principle', 'model', 'framework', 'paradigm']
        content_lower = content.lower()
        keyword_count = sum(
            1 for keyword in concept_keywords if keyword.lower() in content_lower)
        word_count = len(re.findall(r'\w+', content))
        return keyword_count / word_count if word_count > 0 else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        implementation_keywords = [
            'implementation', 'detail', 'step', 'procedure', 'how to', 'example']
        content_lower = content.lower()
        keyword_count = sum(
            1 for keyword in implementation_keywords if keyword.lower() in content_lower)
        word_count = len(re.findall(r'\w+', content))
        return keyword_count / word_count if word_count > 0 else 0.0
