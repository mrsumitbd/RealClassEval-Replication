import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Semantic indicators for different document types
    _DOC_TYPE_INDICATORS = {
        'research_paper': [
            'abstract', 'introduction', 'methodology', 'results', 'discussion', 'conclusion', 'references', 'experiment', 'study', 'analysis', 'dataset', 'proposed', 'findings'
        ],
        'technical_specification': [
            'specification', 'requirements', 'architecture', 'protocol', 'interface', 'implementation', 'compliance', 'standard', 'design', 'overview', 'scope', 'definitions'
        ],
        'tutorial': [
            'step by step', 'how to', 'walkthrough', 'guide', 'example', 'demonstration', 'instructions', 'lesson', 'practice', 'exercise', 'learn', 'introduction'
        ],
        'code_documentation': [
            'function', 'class', 'parameter', 'return', 'example', 'usage', 'api', 'arguments', 'raises', 'attributes', 'module', 'type', 'default'
        ],
        'report': [
            'executive summary', 'findings', 'recommendations', 'analysis', 'background', 'objective', 'scope', 'conclusion', 'appendix', 'methodology'
        ],
        'manual': [
            'user guide', 'installation', 'setup', 'troubleshooting', 'instructions', 'operation', 'maintenance', 'safety', 'warranty', 'configuration'
        ],
        'blog_post': [
            'opinion', 'thoughts', 'insights', 'personal', 'story', 'experience', 'tips', 'tricks', 'reflection', 'perspective', 'introduction'
        ],
    }

    # Segmentation strategies for document types
    _SEGMENTATION_STRATEGIES = {
        'research_paper': 'semantic_sections',
        'technical_specification': 'requirement_blocks',
        'tutorial': 'stepwise',
        'code_documentation': 'api_blocks',
        'report': 'sectional',
        'manual': 'procedure_blocks',
        'blog_post': 'paragraphs'
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        scores = {}
        for doc_type, indicators in self._DOC_TYPE_INDICATORS.items():
            score = self._calculate_weighted_score(
                content, {doc_type: indicators})
            scores[doc_type] = score
        best_type = max(scores, key=scores.get)
        return best_type, scores[best_type]

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        content_lower = content.lower()
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            score = self._detect_pattern_score(content_lower, patterns)
            total_score += score
        # Normalize by number of patterns
        num_patterns = sum(len(p) for p in indicators.values())
        return total_score / num_patterns if num_patterns else 0.0

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0.0
        for pattern in patterns:
            # Use word boundaries for multi-word patterns, else simple word search
            if ' ' in pattern:
                regex = re.compile(
                    r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
            else:
                regex = re.compile(
                    r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
            matches = regex.findall(content)
            if matches:
                score += len(matches)
        return float(score)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        # If doc_type is recognized, use the mapped strategy
        if doc_type in self._SEGMENTATION_STRATEGIES:
            return self._SEGMENTATION_STRATEGIES[doc_type]
        # Fallback: guess based on content
        if self._calculate_algorithm_density(content) > 0.2:
            return 'code_blocks'
        if self._calculate_concept_complexity(content) > 0.5:
            return 'semantic_sections'
        return 'paragraphs'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        # Heuristic: count code-like blocks or algorithm keywords
        code_keywords = ['def ', 'class ', 'function ', 'algorithm', 'procedure',
                         'pseudo', 'input:', 'output:', 'return', 'for ', 'while ', 'if ', 'else']
        code_count = sum(
            len(re.findall(re.escape(kw), content, re.IGNORECASE)) for kw in code_keywords)
        total_words = len(content.split())
        return code_count / total_words if total_words else 0.0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Heuristic: count unique technical terms and average sentence length
        technical_terms = [
            'algorithm', 'complexity', 'architecture', 'framework', 'protocol', 'model', 'dataset', 'evaluation', 'optimization', 'parameter', 'hyperparameter', 'convergence', 'distribution', 'variance', 'regression', 'classification', 'embedding', 'representation', 'ablation', 'baseline', 'metric'
        ]
        term_count = sum(1 for term in technical_terms if re.search(
            r'\b' + re.escape(term) + r'\b', content, re.IGNORECASE))
        sentences = re.split(r'[.!?]', content)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip(
        )) / max(1, len([s for s in sentences if s.strip()]))
        # Normalize: term_count/len(technical_terms) + avg_sentence_length/30 (assuming 30 is a long sentence)
        return 0.5 * (term_count / len(technical_terms)) + 0.5 * min(avg_sentence_length / 30.0, 1.0)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        # Heuristic: count code snippets and implementation words
        impl_words = ['implementation', 'code', 'snippet', 'example', 'usage', 'parameter',
                      'argument', 'return', 'output', 'input', 'variable', 'type', 'default']
        impl_count = sum(len(re.findall(r'\b' + re.escape(word) +
                         r'\b', content, re.IGNORECASE)) for word in impl_words)
        code_blocks = len(re.findall(r'```[\s\S]*?```', content))
        total_words = len(content.split())
        return (impl_count + 2 * code_blocks) / total_words if total_words else 0.0
