
from typing import List, Dict, Any


class NotesSearchController:

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
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
        return [token.lower() for token in query.strip().split() if token]

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        title = note.get('title', '')
        content = note.get('content', '')
        title_tokens = [token.lower()
                        for token in title.strip().split() if token]
        content_tokens = [token.lower()
                          for token in content.strip().split() if token]
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        if not query_tokens:
            return 0.0
        title_matches = sum(
            1 for token in query_tokens if token in title_tokens)
        content_matches = sum(
            1 for token in query_tokens if token in content_tokens)
        # Give higher weight to title matches
        score = title_matches * 2 + content_matches
        return float(score)
