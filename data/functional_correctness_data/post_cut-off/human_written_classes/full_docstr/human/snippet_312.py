from typing import Any, Dict, List

class NotesSearchController:
    """Handles notes search logic and scoring."""

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        """
        search_results = []
        query_tokens = self._process_query(query)
        if not query_tokens:
            return []
        for note in notes:
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(query_tokens, title_tokens, content_tokens)
            if score >= 0.5:
                search_results.append({'id': note.get('id'), 'title': note.get('title'), 'category': note.get('category'), 'modified': note.get('modified'), '_score': score})
        search_results.sort(key=lambda x: x['_score'], reverse=True)
        return search_results

    def _process_query(self, query: str) -> List[str]:
        """
        Tokenize and normalize the search query.
        """
        tokens = query.lower().split()
        tokens = [token for token in tokens if len(token) > 1]
        return tokens

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        """
        Tokenize and normalize note title and content.
        """
        title = note.get('title', '').lower()
        title_tokens = title.split()
        content = note.get('content', '').lower()
        content_tokens = content.split()
        return (title_tokens, content_tokens)

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        """
        Calculate a relevance score for a note based on query tokens.
        """
        TITLE_WEIGHT = 3.0
        CONTENT_WEIGHT = 1.0
        score = 0.0
        title_matches = sum((1 for qt in query_tokens if qt in title_tokens))
        if query_tokens:
            title_match_ratio = title_matches / len(query_tokens)
            score += TITLE_WEIGHT * title_match_ratio
        content_matches = sum((1 for qt in query_tokens if qt in content_tokens))
        if query_tokens:
            content_match_ratio = content_matches / len(query_tokens)
            score += CONTENT_WEIGHT * content_match_ratio
        if title_matches == 0 and content_matches == 0:
            return 0.0
        return score