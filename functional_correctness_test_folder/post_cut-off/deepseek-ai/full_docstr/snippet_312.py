
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
        if not query or not notes:
            return []

        query_tokens = self._process_query(query)
        scored_notes = []

        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                scored_notes.append((score, note))

        scored_notes.sort(key=lambda x: x[0], reverse=True)
        return [note for score, note in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        tokens = re.findall(r'\w+', query.lower())
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = note.get('title', '')
        content = note.get('content', '')

        title_tokens = re.findall(r'\w+', title.lower())
        content_tokens = re.findall(r'\w+', content.lower())

        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not query_tokens:
            return 0.0

        title_counter = Counter(title_tokens)
        content_counter = Counter(content_tokens)
        query_counter = Counter(query_tokens)

        title_score = 0.0
        content_score = 0.0

        for token, count in query_counter.items():
            # Higher weight for title matches
            title_score += title_counter.get(token, 0) * count * 2.0
            content_score += content_counter.get(token, 0) * count

        total_score = title_score + content_score
        return total_score
