
import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = {
            'technical': ['algorithm', 'implementation', 'complexity', 'code', 'function', 'class'],
            'academic': ['research', 'study', 'experiment', 'hypothesis', 'conclusion', 'bibliography'],
            'literary': ['narrative', 'character', 'setting', 'plot', 'theme', 'dialogue'],
            'news': ['report', 'article', 'headline', 'interview', 'opinion', 'editorial']
        }
        scores = {doc_type: self._calculate_weighted_score(
            content, {doc_type: patterns}) for doc_type, patterns in indicators.items()}
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
            matches = re.findall(r'\b' + re.escape(pattern) +
                                 r'\b', content, re.IGNORECASE)
            score += len(matches)
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == 'technical':
            return 'code_block'
        elif doc_type == 'academic':
            return 'paragraph'
        elif doc_type == 'literary':
            return 'scene'
        elif doc_type == 'news':
            return 'section'
        else:
            return 'default'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        code_keywords = ['function', 'class', 'def', 'return',
                         'if', 'else', 'for', 'while', 'try', 'except']
        code_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, code_keywords)) + r')\b', re.IGNORECASE)
        code_matches = code_pattern.findall(content)
        return len(code_matches) / len(content.split()) if content.split() else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_keywords = ['theoretical', 'advanced',
                            'complex', 'sophisticated', 'complicated', 'elaborate']
        complex_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, complex_keywords)) + r')\b', re.IGNORECASE)
        complex_matches = complex_pattern.findall(content)
        return len(complex_matches) / len(content.split()) if content.split() else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ['implementation', 'detail',
                           'specific', 'exact', 'precise', 'detailed']
        detail_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, detail_keywords)) + r')\b', re.IGNORECASE)
        detail_matches = detail_pattern.findall(content)
        return len(detail_matches) / len(content.split()) if content.split() else 0.0
