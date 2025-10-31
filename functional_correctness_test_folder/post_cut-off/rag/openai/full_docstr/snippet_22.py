
import re
import string
from collections import Counter
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Simple keyword sets for a few document types
    _type_indicators: Dict[str, List[str]] = {
        'research_paper': [
            'abstract', 'introduction', 'related work', 'methodology',
            'experiment', 'results', 'conclusion', 'acknowledgement',
            'references', 'doi', 'citation'
        ],
        'blog_post': [
            'introduction', 'summary', 'personal', 'opinion',
            'experience', 'thoughts', 'readers', 'comment', 'share'
        ],
        'technical_report': [
            'executive summary', 'background', 'scope', 'method',
            'findings', 'recommendations', 'appendix', 'figures',
            'tables', 'references'
        ],
        'novel': [
            'chapter', 'protagonist', 'setting', 'dialogue',
            'plot', 'character', 'conflict', 'resolution',
            'theme', 'literary'
        ],
    }

    # Patterns for segmentation strategy hints
    _segmentation_patterns: Dict[str, List[str]] = {
        'research_paper': [
            r'\bAbstract\b', r'\bIntroduction\b', r'\bRelated Work\b',
            r'\bMethodology\b', r'\bExperiments\b', r'\bResults\b',
            r'\bConclusion\b', r'\bReferences\b'
        ],
        'blog_post': [
            r'\bIntroduction\b', r'\bSummary\b', r'\bConclusion\b',
            r'\bRead more\b', r'\bShare\b'
        ],
        'technical_report': [
            r'\bExecutive Summary\b', r'\bBackground\b', r'\bScope\b',
            r'\bMethod\b', r'\bFindings\b', r'\bRecommendations\b',
            r'\bAppendix\b'
        ],
        'novel': [
            r'\bChapter\b', r'\bProtagonist\b', r'\bSetting\b',
            r'\bDialogue\b', r'\bPlot\b', r'\bConflict\b',
            r'\bResolution\b'
        ],
    }

    # Words that indicate algorithmic content
    _algorithm_words = {
        'algorithm', 'pseudocode', 'complexity', 'runtime', 'time',
        'space', 'data structure', 'graph', 'tree', 'queue', 'stack',
        'hash', 'sort', 'search', 'divide', 'conquer', 'dynamic',
        'programming', 'greedy', 'backtracking', 'heuristic'
    }

    # Words that indicate implementation detail
    _implementation_words = {
        'code', 'function', 'class', 'method', 'variable', 'parameter',
        'argument', 'loop', 'if', 'else', 'switch', 'case', 'return',
        'print', 'console', 'debug', 'compile', 'runtime', 'library',
        'framework', 'module', 'package', 'import', 'require'
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        scores = {}
        for doc_type, indicators in self._type_indicators.items():
            scores[doc_type] = self._calculate_weighted_score(
                content, {doc_type: indicators})

        # Normalize scores to [0,1]
        max_score = max(scores.values()) if scores else 0.0
        if max_score == 0:
            return ('unknown', 0.0)

        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / max_score
        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        content_lower = content.lower()
        total_words = len(content_lower.split())
        if total_words == 0:
            return 0.0

        score = 0.0
        for doc_type, words in indicators.items():
            for word in words:
                # Count occurrences of the word as a whole word
                pattern = r'\b' + re.escape(word.lower()) + r'\b'
                matches = re.findall(pattern, content_lower)
                score += len(matches)

        # Normalize by total words to avoid bias toward longer documents
        return score / total_words

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        content_lower = content.lower()
        total_words = len(content_lower.split())
        if total_words == 0:
            return 0.0

        matches = 0
        for pat in patterns:
            if re.search(pat, content, flags=re.IGNORECASE):
                matches += 1

        return matches / len(patterns) if patterns else 0.0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        # Basic heuristic: choose strategy based on density metrics
        algo_density = self._calculate_algorithm_density(content)
        concept_complexity = self._calculate_concept_complexity(content)
        impl_detail = self._calculate_implementation_detail_level(content)

        # Use pattern score to confirm structure
        pattern_score = self._detect_pattern_score(
            content, self._segmentation_patterns.get(doc_type, []))

        # Decide strategy
        if doc_type == 'research_paper':
            if algo_density > 0.05 and pattern_score > 0.5:
                return 'section_based'
            else:
                return 'paragraph_based'
        elif doc_type == 'blog_post':
            if impl_detail > 0.1:
                return 'code_block_based'
            else:
                return 'paragraph_based'
        elif doc_type == 'technical_report':
            if pattern_score > 0.6:
                return 'section_based'
            else:
                return 'paragraph_based'
        elif doc_type == 'novel':
            if concept_complexity > 0.4:
                return 'chapter_based'
            else:
                return 'paragraph_based'
        else:
            # Default fallback
            if pattern_score > 0.3:
                return 'section_based'
            else:
                return 'paragraph_based'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        content_lower = content.lower()
        words = re.findall(r'\b\w+\b', content_lower)
        if not words:
            return 0.0
        algo_count = sum(1 for w in words if w in self._algorithm_words)
        return algo_count / len(words)

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Simple heuristic: average sentence length and number of unique nouns
        sentences = re.split(r'[.!?]\s+', content.strip())
        if not sentences:
            return 0.0
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)

        # Count unique words that are longer than 6 letters (proxy for technical terms)
        words = re.findall(r'\b\w+\b', content.lower())
        unique_long = {w for w in words if len(w) > 6}
        unique_ratio = len(unique_long) / len(set(words)) if words else 0.0

        # Combine metrics
        # normalize roughly to [0,1]
        return (avg_len / 20.0 + unique_ratio) / 2.0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        content_lower = content.lower()
        # Count code fences or inline code markers
        code_fences = len(re.findall(r'
