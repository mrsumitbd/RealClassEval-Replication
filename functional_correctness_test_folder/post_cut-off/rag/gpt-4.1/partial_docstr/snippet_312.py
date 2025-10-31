import re
from typing import List, Dict, Any


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
            if score > 0:
                note_with_score = note.copy()
                note_with_score['_score'] = score
                scored_notes.append(note_with_score)
        scored_notes.sort(key=lambda n: n['_score'], reverse=True)
        return scored_notes

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
        title_matches = sum(
            1 for token in query_tokens if token in title_tokens)
        content_matches = sum(
            1 for token in query_tokens if token in content_tokens)
        # Give higher weight to title matches
        score = 2.0 * title_matches + 1.0 * content_matches
        return score
