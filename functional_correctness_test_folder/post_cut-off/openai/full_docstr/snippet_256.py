
import re
from typing import Dict, Any, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Define regex patterns for common contexts
        self.patterns: Dict[str, re.Pattern] = {
            'weather': re.compile(r'\b(weather|temperature|forecast|rain|sunny|cloudy)\b', re.I),
            'news': re.compile(r'\b(news|headline|article|report|breaking)\b', re.I),
            'stock': re.compile(r'\b(stock|price|ticker|market|shares|NASDAQ|NYSE)\b', re.I),
            'sports': re.compile(r'\b(sport|team|score|match|league|tournament)\b', re.I),
            'travel': re.compile(r'\b(travel|flight|hotel|booking|reservation|airport)\b', re.I),
            'finance': re.compile(r'\b(budget|investment|loan|interest|mortgage)\b', re.I),
            'health': re.compile(r'\b(health|medicine|doctor|symptom|diagnosis|treatment)\b', re.I),
            'technology': re.compile(r'\b(technology|software|hardware|AI|machine learning|algorithm)\b', re.I),
            'education': re.compile(r'\b(education|school|university|course|exam|study)\b', re.I),
            'entertainment': re.compile(r'\b(entertainment|movie|music|concert|festival|show)\b', re.I),
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        if not prompt:
            return {
                'patterns': [],
                'entities': [],
                'confidence': 0.0,
                'tool': tool_name,
                'arguments': arguments,
            }

        # Tokenize prompt for word count
        words = re.findall(r'\b\w+\b', prompt)
        total_words = len(words) or 1  # avoid division by zero

        matched_patterns: List[str] = []
        pattern_confidences: List[float] = []

        # Detect patterns
        for name, regex in self.patterns.items():
            matches = regex.findall(prompt)
            if matches:
                matched_patterns.append(name)
                # Confidence for this pattern: proportion of matched words
                pattern_confidences.append(len(matches) / total_words)

        # Overall confidence: average of pattern confidences (or 0 if none)
        overall_confidence = (
            sum(pattern_confidences) /
            len(pattern_confidences) if pattern_confidences else 0.0
        )

        # Simple entity extraction: capitalized words (excluding first word)
        entities = [
            word for word in re.findall(r'\b[A-Z][a-zA-Z]+\b', prompt)
            if word.lower() not in {'I', 'It', 'The', 'And', 'Or', 'But'}
        ]

        return {
            'patterns': matched_patterns,
            'entities': entities,
            'confidence': round(overall_confidence, 3),
            'tool': tool_name,
            'arguments': arguments,
        }
