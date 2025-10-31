import re
from typing import Any, Dict, List


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        if not notes:
            return []

        query_tokens = self._process_query(query or "")
        if not query_tokens:
            return notes

        ranked: List[tuple[float, int, Dict[str, Any]]] = []
        for idx, note in enumerate(notes):
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                ranked.append((score, idx, note))

        ranked.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, _, n in ranked]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        if not query:
            return []
        # Lowercase and split on non-alphanumeric characters (keep unicode word chars)
        tokens = re.findall(r"\w+", query.lower())
        return [t for t in tokens if t]

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = str(note.get('title') or "")
        # Try common keys for content/body/text
        content = note.get('content')
        if content is None:
            content = note.get('body')
        if content is None:
            content = note.get('text')
        if content is None and 'description' in note:
            content = note.get('description')
        content = str(content or "")

        title_tokens = re.findall(r"\w+", title.lower())
        content_tokens = re.findall(r"\w+", content.lower())
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not query_tokens:
            return 0.0

        # preserve order but unique
        q_unique = list(dict.fromkeys(query_tokens))
        q_set = set(q_unique)
        title_set = set(title_tokens)
        content_set = set(content_tokens)

        # Overlap (coverage) - exact matches
        title_overlap = len(q_set & title_set) / len(q_set)
        content_overlap = len(q_set & content_set) / len(q_set)

        # Partial (prefix) matches for tokens not matched exactly
        def partial_ratio(qs: set[str], target_set: set[str]) -> float:
            if not qs:
                return 0.0
            matched = 0
            for qt in qs:
                if any(ts.startswith(qt) for ts in target_set):
                    matched += 1
            return matched / len(q_set)

        title_partial = partial_ratio(q_set - title_set, title_set)
        content_partial = partial_ratio(q_set - content_set, content_set)

        # Term frequency among query tokens
        if title_tokens:
            title_tf = sum(title_tokens.count(t)
                           for t in q_set) / len(title_tokens)
        else:
            title_tf = 0.0
        if content_tokens:
            content_tf = sum(content_tokens.count(t)
                             for t in q_set) / len(content_tokens)
        else:
            content_tf = 0.0

        # Base weighted score
        score = (
            2.0 * title_overlap +
            1.0 * content_overlap +
            0.5 * title_partial +
            0.25 * content_partial +
            0.5 * title_tf +
            0.25 * content_tf
        )

        # Phrase boost (exact substring of original strings)
        title_text = " ".join(title_tokens)
        content_text = " ".join(content_tokens)
        phrase = " ".join(query_tokens).strip()

        if phrase:
            if phrase in title_text:
                score += 1.5
            if phrase in content_text:
                score += 0.5

        return float(score)
