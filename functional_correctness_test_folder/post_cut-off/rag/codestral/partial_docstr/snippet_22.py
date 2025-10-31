
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
            if self._calculate_implementation_detail_level(content) > 0.7:
                return 'detailed_procedure'
            return 'step_by_step'
        elif doc_type == 'scientific_paper':
            if self._calculate_concept_complexity(content) > 0.6:
                return 'conceptual_breakdown'
            return 'section_based'
        elif doc_type == 'software_documentation':
            if self._calculate_algorithm_density(content) > 0.5:
                return 'algorithm_centric'
            return 'component_based'
        elif doc_type == 'legal_document':
            return 'clause_based'
        elif doc_type == 'financial_report':
            return 'metric_based'
        else:
            return 'general_segmentation'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_keywords = ['algorithm', 'pseudocode',
                              'flowchart', 'complexity', 'time complexity']
        content_lower = content.lower()
        matches = sum(
            1 for keyword in algorithm_keywords if keyword in content_lower)
        return matches / len(algorithm_keywords) if algorithm_keywords else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_terms = ['theorem', 'proof', 'hypothesis',
                         'statistical analysis', 'quantitative model']
        content_lower = content.lower()
        matches = sum(1 for term in complex_terms if term in content_lower)
        return matches / len(complex_terms) if complex_terms else 0.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        detail_indicators = ['implementation details', 'code snippet',
                             'configuration steps', 'troubleshooting', 'error handling']
        content_lower = content.lower()
        matches = sum(
            1 for indicator in detail_indicators if indicator in content_lower)
        return matches / len(detail_indicators) if detail_indicators else 0.0
