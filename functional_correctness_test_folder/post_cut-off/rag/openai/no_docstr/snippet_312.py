
import re
from typing import Any, Dict, List, Tuple


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    _token_pattern = re.compile(r"\b\w+\b")

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
            if score > 0:
                # Copy note to avoid mutating input
                note_copy = dict(note)
                note_copy["score"] = score
                scored_notes.append(note_copy)

        # Sort by score descending, then by original order if needed
        scored_notes.sort(key=lambda n: n["score"], reverse=True)
        return scored_notes

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        if not query:
            return []
        tokens = self._token_pattern.findall(query.lower())
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = note.get("title", "") or ""
        content = note.get("content", "") or ""
        title_tokens = self._token_pattern.findall(title.lower())
        content_tokens = self._token_pattern.findall(content.lower())
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not query_tokens:
            return 0.0

        title_set = set(title_tokens)
        content_set = set(content_tokens)

        score = 0.0
        for token in query_tokens:
            if token in title_set:
                score += 2.0  # higher weight for title matches
            elif token in content_set:
                score += 1.0  # lower weight for content matches

        return score
