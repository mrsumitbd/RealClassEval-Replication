
from typing import Tuple, Dict, List
import re
import math


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Predefined semantic indicators for common document types
    _type_indicators: Dict[str, List[str]] = {
        'research_paper': [
            'abstract', 'introduction', 'methodology', 'results', 'conclusion',
            'experiment', 'data', 'analysis', 'hypothesis', 'literature review'
        ],
        'technical_manual': [
            'installation', 'configuration', 'setup', 'usage', 'troubleshooting',
            'command', 'parameter', 'example', 'procedure', 'reference'
        ],
        'blog_post': [
            'introduction', 'personal', 'experience', 'opinion', 'story',
            'tips', 'tricks', 'guide', 'review', 'summary'
        ],
        'legal_document': [
            'agreement', 'party', 'terms', 'conditions', 'obligation',
            'liability', 'warranty', 'jurisdiction', 'clause', 'amendment'
        ]
    }

    # Semantic patterns for segmentation strategy
    _segmentation_patterns: Dict[str, List[str]] = {
        'paragraph': [r'\n{2,}', r'\n\n'],
        'section': [r'^[A-Z][a-z]+', r'^[0-9]+\.\s'],
        'sentence': [r'\.\s', r'\?\s', r'!\s']
    }

    # Word lists for density calculations
    _algorithm_words = {
        'algorithm', 'function', 'procedure', 'loop', 'recursive', 'iteration',
        'condition', 'branch', 'array', 'list', 'dictionary', 'hash', 'sort',
        'search', 'graph', 'tree', 'node', 'edge', 'path', 'complexity'
    }
    _concept_words = {
        'concept', 'principle', 'theory', 'model', 'framework', 'architecture',
        'design', 'pattern', 'strategy', 'approach', 'method', 'technique',
        'paradigm', 'hypothesis', 'variable', 'parameter', 'metric'
    }
    _implementation_words = {
        'implementation', 'code', 'snippet', 'example', 'sample', 'demo',
        'prototype', 'module', 'class', 'object', 'method', 'function',
        'library', 'framework', 'API', 'interface', 'protocol', 'standard'
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        """
        scores = {}
        for doc_type, indicators in self._type_indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: indicators})

        best_type = max(scores, key=scores.get)
        confidence = min(max(scores[best_type], 0.0), 1.0)
        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate weighted semantic indicator scores"""
        total_score = 0.0
        total_weight = 0.0
        words = re.findall(r'\b\w+\b', content.lower())
        word_set = set(words)
        for doc_type, words_list in indicators.items():
            weight = 0.0
            for w in words_list:
                if w in word_set:
                    weight += 1
            total_score += weight
            total_weight += len(words_list)
        return total_score / total_weight if total_weight else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """Detect semantic pattern matching scores"""
        matches = 0
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE):
                matches += 1
        return matches / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Intelligently determine the best segmentation strategy based on content semantics
        """
        # Prefer section-based segmentation for technical manuals and research papers
        if doc_type in ('technical_manual', 'research_paper'):
            strategy = 'section'
        else:
            # Evaluate pattern scores
            scores = {k: self._detect_pattern_score(
                content, v) for k, v in self._segmentation_patterns.items()}
            strategy = max(scores, key=scores.get)
        return strategy

    def _calculate_algorithm_density(self, content: str) -> float:
        """Calculate algorithm content density"""
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        alg_count = sum(1 for w in words if w in self._algorithm_words)
        return alg_count / len(words)

    def _calculate_concept_complexity(self, content: str) -> float:
        """Calculate concept complexity"""
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        concept_count = sum(1 for w in words if w in self._concept_words)
        return concept_count / len(words)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """Calculate implementation detail level"""
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        impl_count = sum(1 for w in words if w in self._implementation_words)
        return impl_count / len(words)
