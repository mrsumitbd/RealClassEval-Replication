
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
            'technical_manual': ['procedure', 'step', 'installation', 'maintenance', 'specification'],
            'scientific_paper': ['abstract', 'methodology', 'results', 'conclusion', 'literature review'],
            'software_documentation': ['function', 'class', 'module', 'api', 'parameter'],
            'legal_document': ['contract', 'agreement', 'clause', 'article', 'warranty'],
            'financial_report': ['revenue', 'profit', 'expense', 'balance sheet', 'cash flow']
        }

        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: patterns})

        if not scores:
            return ('unknown', 0.0)

        best_match = max(scores.items(), key=lambda x: x[1])
        return best_match

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content, patterns)
            total_score += pattern_score

        return total_score / len(indicators) if indicators else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        if not patterns:
            return 0.0

        content_lower = content.lower()
        matches = sum(1 for pattern in patterns if pattern.lower()
                      in content_lower)
        return matches / len(patterns)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == 'technical_manual':
            return 'procedural_segmentation'
        elif doc_type == 'scientific_paper':
            return 'conceptual_segmentation'
        elif doc_type == 'software_documentation':
            return 'hierarchical_segmentation'
        elif doc_type == 'legal_document':
            return 'clause_based_segmentation'
        elif doc_type == 'financial_report':
            return 'data_driven_segmentation'
        else:
            return 'default_segmentation'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_keywords = ['algorithm', 'pseudocode', 'procedure',
                              'step', 'function', 'loop', 'if', 'else', 'return']
        content_lower = content.lower()
        matches = sum(
            1 for keyword in algorithm_keywords if keyword in content_lower)
        return matches / len(algorithm_keywords) if algorithm_keywords else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_keywords = ['theorem', 'proof', 'lemma', 'corollary',
                            'hypothesis', 'variable', 'equation', 'formula']
        content_lower = content.lower()
        matches = sum(
            1 for keyword in complex_keywords if keyword in content_lower)
        return matches / len(complex_keywords) if complex_keywords else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_keywords = ['implementation', 'detail', 'code',
                           'snippet', 'example', 'pseudocode', 'step-by-step']
        content_lower = content.lower()
        matches = sum(
            1 for keyword in detail_keywords if keyword in content_lower)
        return matches / len(detail_keywords) if detail_keywords else 0.0
