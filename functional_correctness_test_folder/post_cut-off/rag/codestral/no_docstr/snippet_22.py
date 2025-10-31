
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
            'scientific_paper': ['abstract', 'introduction', 'methodology', 'results', 'conclusion'],
            'algorithm_description': ['algorithm', 'pseudocode', 'complexity', 'time', 'space'],
            'tutorial': ['tutorial', 'guide', 'example', 'demo', 'walkthrough'],
            'reference_manual': ['reference', 'syntax', 'function', 'parameter', 'return']
        }

        scores = {}
        for doc_type, patterns in indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: patterns})

        best_match = max(scores.items(), key=lambda x: x[1])
        return best_match[0], best_match[1]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            pattern_score = self._detect_pattern_score(content, patterns)
            total_score += pattern_score * len(patterns)

        return total_score / len(indicators) if indicators else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        content_lower = content.lower()
        matches = sum(1 for pattern in patterns if re.search(
            r'\b' + re.escape(pattern.lower()) + r'\b', content_lower))
        return matches / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        if doc_type == 'algorithm_description':
            algorithm_density = self._calculate_algorithm_density(content)
            if algorithm_density > 0.7:
                return 'algorithm_centric'
            elif algorithm_density > 0.4:
                return 'hybrid'
            else:
                return 'conceptual'

        concept_complexity = self._calculate_concept_complexity(content)
        implementation_detail = self._calculate_implementation_detail_level(
            content)

        if concept_complexity > 0.6 and implementation_detail < 0.3:
            return 'conceptual'
        elif concept_complexity > 0.4 and implementation_detail > 0.4:
            return 'hybrid'
        else:
            return 'detailed'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_keywords = ['algorithm', 'pseudocode', 'complexity',
                              'time', 'space', 'loop', 'if', 'else', 'function', 'procedure']
        total_words = len(content.split())
        if total_words == 0:
            return 0.0

        matches = sum(1 for keyword in algorithm_keywords if re.search(
            r'\b' + re.escape(keyword.lower()) + r'\b', content.lower()))
        return matches / total_words

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        complex_concepts = ['theorem', 'proof', 'lemma', 'corollary',
                            'hypothesis', 'variable', 'parameter', 'equation', 'formula']
        total_words = len(content.split())
        if total_words == 0:
            return 0.0

        matches = sum(1 for concept in complex_concepts if re.search(
            r'\b' + re.escape(concept.lower()) + r'\b', content.lower()))
        return matches / total_words

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        implementation_keywords = ['implementation', 'code', 'snippet', 'example',
                                   'demo', 'walkthrough', 'step', 'procedure', 'installation', 'configuration']
        total_words = len(content.split())
        if total_words == 0:
            return 0.0

        matches = sum(1 for keyword in implementation_keywords if re.search(
            r'\b' + re.escape(keyword.lower()) + r'\b', content.lower()))
        return matches / total_words
