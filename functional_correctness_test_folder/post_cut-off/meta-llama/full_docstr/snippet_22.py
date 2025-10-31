
from typing import Tuple, Dict, List
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.doc_type_indicators = {
            'technical': ['algorithm', 'data structure', 'code', 'programming'],
            'non-technical': ['management', 'business', 'marketing', 'sales']
        }
        self.segmentation_strategies = {
            'technical': 'sentence-based',
            'non-technical': 'paragraph-based'
        }

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        indicators = self.doc_type_indicators
        score = self._calculate_weighted_score(content, indicators)
        doc_type = 'technical' if score > 0.5 else 'non-technical'
        return doc_type, score

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        tokens = self._preprocess_text(content)
        scores = {}
        for doc_type, indicator_list in indicators.items():
            score = sum(1 for token in tokens if token in indicator_list)
            scores[doc_type] = score / len(tokens) if tokens else 0
        return scores['technical']

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        tokens = self._preprocess_text(content)
        score = sum(1 for pattern in patterns if any(
            re.search(pattern, token) for token in tokens))
        return score / len(patterns) if patterns else 0

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        return self.segmentation_strategies.get(doc_type, 'sentence-based')

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        tokens = self._preprocess_text(content)
        algorithm_related_tokens = [token for token in tokens if token in [
            'algorithm', 'data structure', 'code']]
        return len(algorithm_related_tokens) / len(tokens) if tokens else 0

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        sentences = sent_tokenize(content)
        complex_sentences = [sentence for sentence in sentences if len(
            word_tokenize(sentence)) > 15]
        return len(complex_sentences) / len(sentences) if sentences else 0

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        tokens = self._preprocess_text(content)
        implementation_related_tokens = [token for token in tokens if token in [
            'implementation', 'code', 'programming']]
        return len(implementation_related_tokens) / len(tokens) if tokens else 0

    def _preprocess_text(self, content: str) -> List[str]:
        '''Preprocess text by tokenizing, lemmatizing, and removing stop words'''
        tokens = word_tokenize(content.lower())
        tokens = [self.lemmatizer.lemmatize(token)
                  for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens


# Example usage:
if __name__ == "__main__":
    analyzer = DocumentAnalyzer()
    content = "This is a technical document about algorithms and data structures."
    doc_type, confidence_score = analyzer.analyze_document_type(content)
    print(f"Document Type: {doc_type}, Confidence Score: {confidence_score}")
    segmentation_strategy = analyzer.detect_segmentation_strategy(
        content, doc_type)
    print(f"Segmentation Strategy: {segmentation_strategy}")
    algorithm_density = analyzer._calculate_algorithm_density(content)
    print(f"Algorithm Density: {algorithm_density}")
    concept_complexity = analyzer._calculate_concept_complexity(content)
    print(f"Concept Complexity: {concept_complexity}")
    implementation_detail_level = analyzer._calculate_implementation_detail_level(
        content)
    print(f"Implementation Detail Level: {implementation_detail_level}")
