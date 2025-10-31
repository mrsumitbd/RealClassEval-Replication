from typing import Dict, List, Tuple
import re

class DocumentAnalyzer:
    """Enhanced document analyzer using semantic content analysis instead of mechanical structure detection"""
    ALGORITHM_INDICATORS = {'high': ['algorithm', 'procedure', 'method', 'approach', 'technique', 'framework'], 'medium': ['step', 'process', 'implementation', 'computation', 'calculation'], 'low': ['example', 'illustration', 'demonstration']}
    TECHNICAL_CONCEPT_INDICATORS = {'high': ['formula', 'equation', 'theorem', 'lemma', 'proof', 'definition'], 'medium': ['parameter', 'variable', 'function', 'model', 'architecture'], 'low': ['notation', 'symbol', 'term']}
    IMPLEMENTATION_INDICATORS = {'high': ['code', 'implementation', 'programming', 'software', 'system'], 'medium': ['design', 'structure', 'module', 'component', 'interface'], 'low': ['tool', 'library', 'package']}
    RESEARCH_PAPER_PATTERNS = ['(?i)\\babstract\\b.*?\\n.*?(introduction|motivation|background)', '(?i)(methodology|method).*?(experiment|evaluation|result)', '(?i)(conclusion|future work|limitation).*?(reference|bibliography)', '(?i)(related work|literature review|prior art)']
    TECHNICAL_DOC_PATTERNS = ['(?i)(getting started|installation|setup).*?(usage|example)', '(?i)(api|interface|specification).*?(parameter|endpoint)', '(?i)(tutorial|guide|walkthrough).*?(step|instruction)', '(?i)(troubleshooting|faq|common issues)']

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        """
        Enhanced document type analysis based on semantic content patterns

        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        """
        content_lower = content.lower()
        algorithm_score = self._calculate_weighted_score(content_lower, self.ALGORITHM_INDICATORS)
        concept_score = self._calculate_weighted_score(content_lower, self.TECHNICAL_CONCEPT_INDICATORS)
        implementation_score = self._calculate_weighted_score(content_lower, self.IMPLEMENTATION_INDICATORS)
        research_pattern_score = self._detect_pattern_score(content, self.RESEARCH_PAPER_PATTERNS)
        technical_pattern_score = self._detect_pattern_score(content, self.TECHNICAL_DOC_PATTERNS)
        total_research_score = algorithm_score + concept_score + research_pattern_score * 2
        total_technical_score = implementation_score + technical_pattern_score * 2
        if research_pattern_score > 0.5 and total_research_score > 3.0:
            return ('research_paper', min(0.95, 0.6 + research_pattern_score * 0.35))
        elif algorithm_score > 2.0 and concept_score > 1.5:
            return ('algorithm_focused', 0.85)
        elif total_technical_score > 2.5:
            return ('technical_doc', 0.8)
        elif implementation_score > 1.5:
            return ('implementation_guide', 0.75)
        else:
            return ('general_document', 0.5)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        """Calculate weighted semantic indicator scores"""
        score = 0.0
        for weight_level, terms in indicators.items():
            weight = {'high': 3.0, 'medium': 2.0, 'low': 1.0}[weight_level]
            for term in terms:
                if term in content:
                    score += weight * (content.count(term) * 0.5 + 1)
        return score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        """Detect semantic pattern matching scores"""
        matches = 0
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL):
                matches += 1
        return matches / len(patterns)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        """
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        """
        algorithm_density = self._calculate_algorithm_density(content)
        concept_complexity = self._calculate_concept_complexity(content)
        implementation_detail_level = self._calculate_implementation_detail_level(content)
        if doc_type == 'research_paper' and algorithm_density > 0.3:
            return 'semantic_research_focused'
        elif doc_type == 'algorithm_focused' or algorithm_density > 0.5:
            return 'algorithm_preserve_integrity'
        elif concept_complexity > 0.4 and implementation_detail_level > 0.3:
            return 'concept_implementation_hybrid'
        elif len(content) > 15000:
            return 'semantic_chunking_enhanced'
        else:
            return 'content_aware_segmentation'

    def _calculate_algorithm_density(self, content: str) -> float:
        """Calculate algorithm content density"""
        total_chars = len(content)
        algorithm_chars = 0
        algorithm_patterns = ['(?i)(algorithm\\s+\\d+|procedure\\s+\\d+)', '(?i)(step\\s+\\d+|phase\\s+\\d+)', '(?i)(input:|output:|return:|initialize:)', '(?i)(for\\s+each|while|if.*then|else)', '(?i)(function|method|procedure).*\\(']
        for pattern in algorithm_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 800)
                algorithm_chars += end - start
        return min(1.0, algorithm_chars / total_chars)

    def _calculate_concept_complexity(self, content: str) -> float:
        """Calculate concept complexity"""
        concept_indicators = self.TECHNICAL_CONCEPT_INDICATORS
        complexity_score = 0.0
        for level, terms in concept_indicators.items():
            weight = {'high': 3.0, 'medium': 2.0, 'low': 1.0}[level]
            for term in terms:
                complexity_score += content.lower().count(term) * weight
        return min(1.0, complexity_score / 100)

    def _calculate_implementation_detail_level(self, content: str) -> float:
        """Calculate implementation detail level"""
        implementation_patterns = ['(?i)(code|implementation|programming)', '(?i)(class|function|method|variable)', '(?i)(import|include|library)', '(?i)(parameter|argument|return)', '(?i)(example|demo|tutorial)']
        detail_score = 0
        for pattern in implementation_patterns:
            detail_score += len(re.findall(pattern, content))
        return min(1.0, detail_score / 50)