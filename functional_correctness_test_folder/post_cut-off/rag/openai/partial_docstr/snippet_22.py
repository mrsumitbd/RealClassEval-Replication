import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Predefined semantic indicators for common document types
    _TYPE_INDICATORS: Dict[str, List[str]] = {
        'research_paper': [
            'abstract', 'introduction', 'related work', 'methodology',
            'experiment', 'results', 'conclusion', 'acknowledgement',
            'references', 'bibliography'
        ],
        'blog_post': [
            'introduction', 'summary', 'call to action', 'personal',
            'experience', 'tips', 'tricks', 'how to', 'guide'
        ],
        'technical_report': [
            'executive summary', 'background', 'scope', 'method',
            'analysis', 'findings', 'recommendations', 'appendix'
        ],
        'novel': [
            'chapter', 'protagonist', 'setting', 'dialogue', 'plot',
            'conflict', 'resolution', 'theme'
        ],
        'manual': [
            'installation', 'setup', 'configuration', 'usage',
            'commands', 'parameters', 'examples', 'faq'
        ]
    }

    # Simple semantic patterns for segmentation strategy
    _SEGMENT_PATTERNS: Dict[str, List[str]] = {
        'algorithmic': [
            'algorithm', 'pseudocode', 'complexity', 'time', 'space',
            'runtime', 'proof', 'lemma', 'theorem'
        ],
        'conceptual': [
            'definition', 'concept', 'principle', 'theory', 'model',
            'framework', 'approach', 'hypothesis'
        ],
        'implementation': [
            'code', 'function', 'class', 'module', 'library',
            'syntax', 'example', 'snippet'
        ]
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        content_lower = content.lower()
        scores = {}
        for doc_type, indicators in self._TYPE_INDICATORS.items():
            scores[doc_type] = self._calculate_weighted_score(
                content_lower, {doc_type: indicators})
        # Normalize scores to [0,1]
        max_score = max(scores.values()) if scores else 0.0
        if max_score == 0:
            return ('unknown', 0.0)
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / max_score
        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        score = 0.0
        for indicator_list in indicators.values():
            for keyword in indicator_list:
                # Count whole word occurrences
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = re.findall(pattern, content)
                score += len(matches)
        return score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        for pattern in patterns:
            # Simple substring search; could be regex
            if pattern.lower() in content.lower():
                score += 1.0
        return score

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        # Compute densities for each strategy
        densities = {}
        for strategy, patterns in self._SEGMENT_PATTERNS.items():
            densities[strategy] = self._detect_pattern_score(content, patterns)

        # Adjust densities based on overall content characteristics
        algorithm_density = self._calculate_algorithm_density(content)
        concept_complexity = self._calculate_concept_complexity(content)
        implementation_level = self._calculate_implementation_detail_level(
            content)

        # Weight adjustments
        densities['algorithmic'] += algorithm_density * 0.5
        densities['conceptual'] += concept_complexity * 0.5
        densities['implementation'] += implementation_level * 0.5

        # Choose strategy with highest density
        best_strategy = max(densities, key=densities.get)
        return best_strategy

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algorithm_terms = [
            'algorithm', 'pseudocode', 'complexity', 'runtime',
            'time', 'space', 'proof', 'lemma', 'theorem'
        ]
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
        term_count = sum(content.lower().count(term)
                         for term in algorithm_terms)
        return term_count / total_words

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        advanced_terms = [
            'theorem', 'lemma', 'corollary', 'axiom', 'hypothesis',
            'principle', 'framework', 'paradigm', 'ontology'
        ]
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
        term_count = sum(content.lower().count(term)
                         for term in advanced_terms)
        return term_count / total_words

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        code_indicators = [
            'def ', 'class ', 'import ', 'function', 'int(', 'float(',
            'print(', 'return ', 'if ', 'for ', 'while ', 'try:', 'except:'
        ]
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
        indicator_count = sum(content.lower().count(ind)
                              for ind in code_indicators)
        return indicator_count / total_words
