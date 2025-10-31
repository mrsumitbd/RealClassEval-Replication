import re
from typing import Dict, List, Tuple


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    # Semantic indicator patterns for different document types
    _DOC_TYPE_INDICATORS = {
        'research_paper': [
            r'\babstract\b', r'\bmethodology\b', r'\bresults?\b', r'\bconclusion\b', r'\breferences?\b',
            r'\bexperiment(s)?\b', r'\bstatistical analysis\b', r'\bintroduction\b'
        ],
        'technical_specification': [
            r'\brequirements?\b', r'\barchitecture\b', r'\binterface\b', r'\bprotocol\b', r'\bimplementation\b',
            r'\bconfiguration\b', r'\bparameters?\b', r'\bworkflow\b'
        ],
        'tutorial': [
            r'\bstep[- ]by[- ]step\b', r'\bexample\b', r'\bwalkthrough\b', r'\bhow to\b', r'\bguide\b',
            r'\btutorial\b', r'\bexercise\b', r'\bpractice\b'
        ],
        'manual': [
            r'\binstruction\b', r'\buser guide\b', r'\bmanual\b', r'\btroubleshooting\b', r'\bfaq\b',
            r'\bsetup\b', r'\binstallation\b', r'\bmaintenance\b'
        ],
        'report': [
            r'\bexecutive summary\b', r'\bfindings\b', r'\brecommendations?\b', r'\bappendix\b', r'\bdata analysis\b',
            r'\bbackground\b', r'\bdiscussion\b'
        ],
        'code_documentation': [
            r'\bapi\b', r'\bclass\b', r'\bfunction\b', r'\bparameters?\b', r'\breturns?\b', r'\bexample\b',
            r'\busage\b', r'\bmodule\b', r'\bobject\b'
        ],
    }

    # Segmentation strategies for document types
    _SEGMENTATION_STRATEGIES = {
        'research_paper': 'semantic_sections',
        'technical_specification': 'requirement_blocks',
        'tutorial': 'stepwise',
        'manual': 'instructional_blocks',
        'report': 'sectional',
        'code_documentation': 'api_blocks',
        'default': 'paragraph'
    }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        scores = {}
        for doc_type, patterns in self._DOC_TYPE_INDICATORS.items():
            score = self._detect_pattern_score(content, patterns)
            scores[doc_type] = score
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]
        # Normalize confidence to [0,1]
        max_possible = max(len(v) for v in self._DOC_TYPE_INDICATORS.values())
        confidence = min(confidence / max_possible, 1.0)
        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        total_score = 0.0
        total_weight = 0.0
        for key, patterns in indicators.items():
            weight = 1.0
            if key in ('abstract', 'introduction', 'api', 'step-by-step'):
                weight = 1.5  # More important indicators
            score = self._detect_pattern_score(content, patterns)
            total_score += score * weight
            total_weight += len(patterns) * weight
        if total_weight == 0:
            return 0.0
        return total_score / total_weight

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        score = 0
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 1
        return float(score)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        # If doc_type is known, use mapping
        if doc_type in self._SEGMENTATION_STRATEGIES:
            return self._SEGMENTATION_STRATEGIES[doc_type]
        # Fallback: guess based on content
        if re.search(r'\bstep\s*\d+\b', content, re.IGNORECASE):
            return 'stepwise'
        if re.search(r'\bsection\b', content, re.IGNORECASE):
            return 'semantic_sections'
        if re.search(r'\bapi\b', content, re.IGNORECASE):
            return 'api_blocks'
        return self._SEGMENTATION_STRATEGIES['default']

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        # Heuristic: count algorithmic keywords and code blocks
        algo_keywords = [
            r'\balgorithm\b', r'\bprocedure\b', r'\bcomplexity\b', r'\bperformance\b',
            r'\boptimization\b', r'\brecursion\b', r'\biteration\b', r'\bloop\b'
        ]
        code_block_count = len(re.findall(r'```[\s\S]*?```', content))
        keyword_count = sum(1 for pattern in algo_keywords if re.search(
            pattern, content, re.IGNORECASE))
        total = code_block_count + keyword_count
        # Normalize by content length
        norm = len(content.split())
        if norm == 0:
            return 0.0
        return min(total / (norm / 1000), 1.0)

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        # Heuristic: count unique technical terms and average sentence length
        technical_terms = [
            r'\btheorem\b', r'\bcorollary\b', r'\blemma\b', r'\baxiom\b', r'\bproof\b',
            r'\bmodel\b', r'\bframework\b', r'\barchitecture\b', r'\bparadigm\b', r'\bprotocol\b'
        ]
        term_count = sum(1 for pattern in technical_terms if re.search(
            pattern, content, re.IGNORECASE))
        sentences = re.split(r'[.!?]', content)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip(
        )) / max(1, len([s for s in sentences if s.strip()]))
        # Complexity: weighted sum, normalized
        complexity = (term_count * 0.6 + avg_sentence_length * 0.4) / 10.0
        return min(complexity, 1.0)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        # Heuristic: count code blocks, parameter lists, and usage of "implementation" words
        code_blocks = len(re.findall(r'```[\s\S]*?```', content))
        param_mentions = len(re.findall(
            r'\bparameters?\b', content, re.IGNORECASE))
        impl_mentions = len(re.findall(
            r'\bimplementation\b', content, re.IGNORECASE))
        total = code_blocks * 2 + param_mentions + impl_mentions
        norm = len(content.split())
        if norm == 0:
            return 0.0
        return min(total / (norm / 1000), 1.0)
