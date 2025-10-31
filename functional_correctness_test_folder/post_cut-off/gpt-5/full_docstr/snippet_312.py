from typing import List, Dict, Any, Tuple
import re


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    _WORD_RE = re.compile(r"[a-z0-9']+")
    _STOPWORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'in', 'on', 'at', 'to', 'of', 'for', 'with', 'by', 'is', 'it',
        'this', 'that', 'these', 'those', 'as', 'from', 'be', 'are', 'was', 'were', 'been', 'am', 'i', 'you', 'he',
        'she', 'they', 'we', 'me', 'him', 'her', 'them', 'my', 'your', 'his', 'their', 'our', 'so', 'not'
    }

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        if not query_tokens:
            return []

        ranked: List[Tuple[int, float, Dict[str, Any]]] = []
        for idx, note in enumerate(notes):
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                ranked.append((idx, score, note))

        ranked.sort(key=lambda x: (-x[1], x[0]))
        return [n for _, _, n in ranked]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        if not query:
            return []
        tokens = [t for t in self._WORD_RE.findall(
            query.lower()) if t and t not in self._STOPWORDS]
        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for t in tokens:
            if t not in seen:
                seen.add(t)
                deduped.append(t)
        return deduped

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = note.get('title') or ''
        content = note.get('content') or ''
        title_tokens = [t for t in self._WORD_RE.findall(
            str(title).lower()) if t]
        content_tokens = [t for t in self._WORD_RE.findall(
            str(content).lower()) if t]
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not query_tokens:
            return 0.0

        title_counts = {}
        for t in title_tokens:
            title_counts[t] = title_counts.get(t, 0) + 1

        content_counts = {}
        for t in content_tokens:
            content_counts[t] = content_counts.get(t, 0) + 1

        score = 0.0
        matched = 0

        for q in query_tokens:
            t_count = title_counts.get(q, 0)
            c_count = content_counts.get(q, 0)

            if t_count or c_count:
                matched += 1

            # Presence boosts
            if t_count:
                score += 2.0  # title presence boost
            if c_count:
                score += 1.0  # content presence boost

            # Frequency contribution
            score += t_count * 1.0
            score += c_count * 0.25

        # Coverage bonus: how many query terms matched
        coverage = matched / len(query_tokens)
        score *= (1.0 + 0.25 * coverage)

        # Short-title slight bonus if many matches are in a concise title
        if matched and title_tokens:
            unique_title = len(set(title_tokens))
            compactness = min(1.0, matched / max(1, unique_title))
            score += 0.2 * compactness

        return score
