
from typing import List, Dict, Any
import re
from collections import Counter


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        scored_notes = []

        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            scored_notes.append((note, score))

        # Sort notes by score in descending order
        scored_notes.sort(key=lambda x: x[1], reverse=True)
        return [note for note, score in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        return self._tokenize_and_normalize(query)

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = note.get('title', '')
        content = note.get('content', '')
        return self._tokenize_and_normalize(title), self._tokenize_and_normalize(content)

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        title_counter = Counter(title_tokens)
        content_counter = Counter(content_tokens)
        query_counter = Counter(query_tokens)

        title_score = sum(
            query_counter[token] * title_counter[token] for token in query_counter)
        content_score = sum(
            query_counter[token] * content_counter[token] for token in query_counter)

        # Boost score if query tokens appear in the title
        title_score *= 2

        return title_score + content_score

    def _tokenize_and_normalize(self, text: str) -> List[str]:
        '''
        Tokenize and normalize the text.
        '''
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Tokenize
        tokens = text.split()
        return tokens
