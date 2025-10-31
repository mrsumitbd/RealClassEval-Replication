
from typing import Dict, List, Tuple
import re


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = {
            'technical': ['algorithm', 'implementation', 'complexity', 'function', 'method'],
            'legal': ['clause', 'section', 'agreement', 'party', 'law'],
            'academic': ['study', 'research', 'hypothesis', 'results', 'data'],
            'business': ['strategy', 'market', 'growth', 'revenue', 'customer']
        }

        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: patterns})

        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content, patterns)
            total_score += pattern_score
        return total_score / len(indicators) if indicators else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        content_lower = content.lower()
        for pattern in patterns:
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', content_lower):
                score += 1.0
        return score / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == 'technical':
            algo_density = self._calculate_algorithm_density(content)
            if algo_density > 0.5:
                return 'algorithmic_flow'
            else:
                return 'functional_blocks'
        elif doc_type == 'legal':
            return 'section_hierarchy'
        elif doc_type == 'academic':
            concept_complexity = self._calculate_concept_complexity(content)
            if concept_complexity > 0.6:
                return 'concept_dependencies'
            else:
                return 'standard_sections'
        elif doc_type == 'business':
            return 'topic_clusters'
        else:
            return 'default_hierarchy'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algo_keywords = ['algorithm', 'pseudo',
                         'complexity', 'O(', 'step', 'loop']
        matches = sum(
            1 for keyword in algo_keywords if keyword.lower() in content.lower())
        return matches / len(algo_keywords)

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_indicators = ['however', 'although',
                              'therefore', 'thus', 'moreover']
        matches = sum(
            1 for indicator in complex_indicators if indicator.lower() in content.lower())
        return matches / len(complex_indicators)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ['code', 'function',
                           'method', 'class', 'variable', 'parameter']
        matches = sum(
            1 for keyword in detail_keywords if keyword.lower() in content.lower())
        return matches / len(detail_keywords)
