import re
import math
from collections import Counter
from typing import Any, Dict, List


class NotesSearchController:
    '''Handles notes search logic and scoring.'''

    _STOPWORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into',
        'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then',
        'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with', 'from', 'we', 'you',
        'your', 'our', 'i', 'me', 'my', 'mine', 'yours', 'ours', 'he', 'she', 'him', 'her',
        'his', 'hers', 'them', 'they', 'what', 'which', 'who', 'whom', 'why', 'how', 'when',
        'where', 'also', 'too', 'very', 'can', 'could', 'should', 'would', 'do', 'does', 'did'
    }

    def search_notes(self, notes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        '''
        Search notes using token-based matching with relevance ranking.
        Returns notes sorted by relevance score.
        '''
        query_tokens = self._process_query(query)
        if not query_tokens:
            return []

        scored: List[tuple[float, int, Dict[str, Any]]] = []
        for idx, note in enumerate(notes):
            if not isinstance(note, dict):
                continue
            title_tokens, content_tokens = self._process_note_content(note)
            score = self._calculate_score(
                query_tokens, title_tokens, content_tokens)
            if score > 0:
                # Tie-breakers: higher score first, then earlier index (stable), then title lexicographically
                scored.append((score, idx, note))

        scored.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, _, n in scored]

    def _process_query(self, query: str) -> List[str]:
        '''
        Tokenize and normalize the search query.
        '''
        if not query:
            return []
        return self._tokenize(query)

    def _process_note_content(self, note: Dict[str, Any]) -> tuple[List[str], List[str]]:
        '''
        Tokenize and normalize note title and content.
        '''
        title = str(note.get('title') or '')
        # Prefer 'content', but fall back to common alternatives
        content = str(
            note.get('content') or
            note.get('body') or
            note.get('text') or
            ''
        )

        title_tokens = self._tokenize(title)
        content_tokens = self._tokenize(content)
        return title_tokens, content_tokens

    def _calculate_score(self, query_tokens: List[str], title_tokens: List[str], content_tokens: List[str]) -> float:
        '''
        Calculate a relevance score for a note based on query tokens.
        '''
        if not query_tokens:
            return 0.0

        q_counter = Counter(query_tokens)
        q_unique = set(q_counter.keys())
        t_counter = Counter(title_tokens)
        c_counter = Counter(content_tokens)

        # Base occurrence scores
        title_weight = 3.0
        content_weight = 1.0

        title_occ = sum(t_counter.get(tok, 0) for tok in q_unique)
        content_occ = sum(c_counter.get(tok, 0) for tok in q_unique)

        base_score = title_weight * title_occ + content_weight * content_occ

        # Coverage (how many unique query tokens are present)
        matched_unique = sum(1 for tok in q_unique if t_counter.get(
            tok, 0) > 0 or c_counter.get(tok, 0) > 0)
        coverage = matched_unique / max(1, len(q_unique))
        coverage_weight = 2.5
        coverage_score = coverage * coverage_weight

        # Phrase/contiguity bonuses
        phrase = ' '.join(query_tokens)
        title_str = ' '.join(title_tokens)
        content_str = ' '.join(content_tokens)

        phrase_bonus = 0.0
        if phrase and phrase in title_str:
            phrase_bonus += 2.0 + 0.5 * min(len(query_tokens) - 1, 4)
        elif phrase and phrase in content_str:
            phrase_bonus += 1.0 + 0.3 * min(len(query_tokens) - 1, 4)

        # All tokens in title bonus
        if q_unique and all(tok in t_counter for tok in q_unique):
            phrase_bonus += 1.25

        # Normalize by content length to avoid bias toward very long notes
        content_len = len(content_tokens)
        norm = 1.0 + math.log(1.0 + max(0, content_len))

        score = (base_score + coverage_score + phrase_bonus) / norm
        return float(score)

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        # Extract alphanumerics and apostrophes within words, then strip apostrophes
        raw_tokens = re.findall(r"[a-z0-9']+", text)
        tokens = [t.strip("'") for t in raw_tokens if t.strip("'")]

        # Remove stopwords and apply light stemming
        processed: List[str] = []
        for tok in tokens:
            if tok in self._STOPWORDS:
                continue
            stemmed = self._light_stem(tok)
            if stemmed and (len(stemmed) > 1 or stemmed.isdigit()):
                processed.append(stemmed)
        return processed

    def _light_stem(self, token: str) -> str:
        # Very lightweight stemming for English-like words
        if len(token) > 4 and token.endswith('ing'):
            return token[:-3]
        if len(token) > 3 and token.endswith('ed'):
            return token[:-2]
        if len(token) > 3 and token.endswith('es'):
            return token[:-2]
        if len(token) > 3 and token.endswith('s'):
            return token[:-1]
        return token
