
from typing import Tuple, Dict, List


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = {
            'technical': ['algorithm', 'data structure', 'implementation'],
            'literary': ['character', 'plot', 'setting'],
            'scientific': ['hypothesis', 'experiment', 'result']
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {doc_type: indicators[doc_type]}) for doc_type in indicators}
        best_match = max(scores, key=scores.get)
        return best_match, scores[best_match]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            total_score += self._detect_pattern_score(content, patterns)
        return total_score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        for pattern in patterns:
            if pattern.lower() in content.lower():
                score += 1.0
        return score / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == 'technical':
            return 'code_block'
        elif doc_type == 'literary':
            return 'paragraph'
        elif doc_type == 'scientific':
            return 'section'
        else:
            return 'default'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_keywords = ['algorithm', 'function', 'procedure']
        return self._detect_pattern_score(content, algorithm_keywords)

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complexity_keywords = ['complexity', 'theoretical', 'advanced']
        return self._detect_pattern_score(content, complexity_keywords)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ['implementation', 'code', 'example']
        return self._detect_pattern_score(content, detail_keywords)
