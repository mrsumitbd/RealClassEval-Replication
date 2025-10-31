import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Semantic indicators for different document types
    _DOC_TYPE_INDICATORS = {
        'research_paper': [
            'abstract', 'introduction', 'methodology', 'results', 'discussion', 'conclusion', 'references', 'experiment', 'dataset', 'analysis', 'statistical', 'significant', 'proposed method', 'related work'
        ],
        'technical_specification': [
            'specification', 'requirements', 'architecture', 'protocol', 'interface', 'implementation', 'compliance', 'standard', 'configuration', 'parameters', 'overview', 'scope', 'definitions'
        ],
        'tutorial': [
            'step by step', 'how to', 'walkthrough', 'example', 'guide', 'instructions', 'demonstration', 'hands-on', 'practice', 'exercise', 'lesson', 'introduction', 'summary'
        ],
        'user_manual': [
            'user guide', 'manual', 'instructions', 'usage', 'operation', 'troubleshooting', 'installation', 'setup', 'maintenance', 'safety', 'warranty', 'support', 'features'
        ],
        'code_documentation': [
            'function', 'class', 'parameter', 'return', 'example', 'usage', 'api', 'reference', 'module', 'attribute', 'exception', 'type', 'signature'
        ],
        'business_report': [
            'executive summary', 'findings', 'recommendations', 'analysis', 'market', 'financial', 'strategy', 'conclusion', 'overview', 'objectives', 'scope', 'methodology'
        ],
        'legal_document': [
            'hereby', 'whereas', 'hereto', 'party', 'agreement', 'contract', 'witnesseth', 'clause', 'obligation', 'liability', 'jurisdiction', 'term', 'condition'
        ],
        'blog_post': [
            'opinion', 'thoughts', 'experience', 'story', 'insight', 'tips', 'tricks', 'personal', 'reflection', 'commentary', 'introduction', 'conclusion'
        ],
    }

    # Segmentation strategies for document types
    _SEGMENTATION_STRATEGIES = {
        'research_paper': 'semantic_sections',
        'technical_specification': 'section_headers',
        'tutorial': 'step_blocks',
        'user_manual': 'task_oriented',
        'code_documentation': 'code_blocks_and_comments',
        'business_report': 'report_sections',
        'legal_document': 'clause_blocks',
        'blog_post': 'paragraphs',
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
        confidence = scores[best_type]
        # Normalize confidence to [0, 1]
        max_possible = max(scores.values()) if scores else 1.0
        norm_conf = confidence / max_possible if max_possible > 0 else 0.0
        return best_type, round(norm_conf, 3)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        content_lower = content.lower()
        total_score = 0.0
        for doc_type, patterns in indicators.items():
            score = self._detect_pattern_score(content_lower, patterns)
            total_score += score
        return total_score

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
            score += len(matches)
        # Weight by number of unique patterns matched
        unique_matches = sum(1 for pattern in patterns if re.search(
            r'\b' + re.escape(pattern) + r'\b', content, re.IGNORECASE))
        return score + 0.5 * unique_matches

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        doc_type = doc_type.lower()
        if doc_type in self._SEGMENTATION_STRATEGIES:
            return self._SEGMENTATION_STRATEGIES[doc_type]
        # Fallback: guess based on content
        if self._calculate_algorithm_density(content) > 0.2:
            return 'code_blocks_and_comments'
        elif self._calculate_concept_complexity(content) > 0.5:
            return 'semantic_sections'
        else:
            return 'paragraphs'

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        # Heuristic: count code-like blocks, pseudocode, or algorithm keywords
        code_keywords = ['def ', 'class ', 'function ', 'algorithm', 'procedure', 'input:',
                         'output:', 'return', 'for ', 'while ', 'if ', 'else', 'elif', 'end', 'begin']
        code_blocks = re.findall(r'```.*?```', content, re.DOTALL)
        code_score = len(code_blocks) * 2
        for kw in code_keywords:
            code_score += len(re.findall(re.escape(kw),
                              content, re.IGNORECASE))
        # Normalize by content length (in 1000s of chars)
        norm = max(1, len(content) // 1000)
        return min(1.0, code_score / (norm * 10))

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Heuristic: count long sentences, technical terms, and unique words
        sentences = re.split(r'[.!?]', content)
        long_sentences = [s for s in sentences if len(s.split()) > 20]
        unique_words = set(re.findall(r'\b\w+\b', content.lower()))
        technical_terms = ['algorithm', 'complexity', 'architecture', 'protocol', 'theorem',
                           'proof', 'analysis', 'implementation', 'optimization', 'framework', 'model', 'dataset']
        tech_term_count = sum(
            1 for term in technical_terms if term in content.lower())
        complexity_score = (len(long_sentences) * 2 +
                            len(unique_words) / 100 + tech_term_count * 3)
        # Normalize
        norm = max(1, len(sentences) / 10)
        return min(1.0, complexity_score / (norm * 10))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        # Heuristic: count code snippets, parameter lists, and configuration details
        code_snippets = re.findall(r'```.*?```', content, re.DOTALL)
        param_patterns = [r'parameter[s]?:', r'argument[s]?:',
                          r'config(uration)?', r'default[s]?:', r'option[s]?:']
        param_count = sum(len(re.findall(pat, content, re.IGNORECASE))
                          for pat in param_patterns)
        detail_score = len(code_snippets) * 2 + param_count
        # Normalize by content length (in 1000s of chars)
        norm = max(1, len(content) // 1000)
        return min(1.0, detail_score / (norm * 8))
