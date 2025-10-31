
from typing import List, Dict, Any
import re


class NotesSearchController:

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
                scored_notes.append((score, note))
        scored_notes.sort(reverse=True, key=lambda x: x[0])
        return [note for score, note in scored_notes]

    def _process_query(self, query: str) -> List[str]:
        tokens = re.findall(r'\w+', query.lower())
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        title = note.get('title', '')
        content = note.get('content', '')
        title_tokens = re.findall(r'\w+', title.lower())
        content_tokens = re.findall(r'\w+', content.lower())
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        if not query_tokens:
            return 0.0
        title_set = set(title_tokens)
        content_set = set(content_tokens)
        score = 0.0
        for token in query_tokens:
            if token in title_set:
                score += 2.0
            if token in content_set:
                score += 1.0
        return score
