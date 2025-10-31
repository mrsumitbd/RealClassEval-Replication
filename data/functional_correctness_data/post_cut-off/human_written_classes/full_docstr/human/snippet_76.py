from memos.embedders.factory import OllamaEmbedder
import uuid
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata
from datetime import datetime

class InternetGoogleRetriever:
    """Internet retriever that converts search results to TextualMemoryItem format"""

    def __init__(self, api_key: str, search_engine_id: str, embedder: OllamaEmbedder, max_results: int=20, num_per_request: int=10):
        """
        Initialize internet retriever

        Args:
            api_key: Google API key
            search_engine_id: Search engine ID
            embedder: Embedder instance for generating embeddings
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        """
        self.google_api = GoogleCustomSearchAPI(api_key, search_engine_id, max_results=max_results, num_per_request=num_per_request)
        self.embedder = embedder

    def retrieve_from_internet(self, query: str, top_k: int=10, parsed_goal=None, info=None) -> list[TextualMemoryItem]:
        """
        Retrieve information from the internet and convert to TextualMemoryItem format

        Args:
            query: Search query
            top_k: Number of results to return
            parsed_goal: Parsed task goal (optional)
            info (dict): Leave a record of memory consumption.

        Returns:
            List of TextualMemoryItem
        """
        if not info:
            info = {'user_id': '', 'session_id': ''}
        search_results = self.google_api.get_all_results(query, max_results=top_k)
        memory_items = []
        for _, result in enumerate(search_results):
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            link = result.get('link', '')
            display_link = result.get('displayLink', '')
            memory_content = f'Title: {title}\nSummary: {snippet}\nSource: {link}'
            metadata = TreeNodeTextualMemoryMetadata(user_id=info.get('user_id', ''), session_id=info.get('session_id', ''), status='activated', type='fact', memory_time=datetime.now().strftime('%Y-%m-%d'), source='web', confidence=85.0, entities=self._extract_entities(title, snippet), tags=self._extract_tags(title, snippet, parsed_goal), visibility='public', memory_type='LongTermMemory', key=title, sources=[link] if link else [], embedding=self.embedder.embed([memory_content])[0], created_at=datetime.now().isoformat(), usage=[], background=f'Internet search result from {display_link}')
            memory_item = TextualMemoryItem(id=str(uuid.uuid4()), memory=memory_content, metadata=metadata)
            memory_items.append(memory_item)
        return memory_items

    def _extract_entities(self, title: str, snippet: str) -> list[str]:
        """
        Extract entities from title and snippet

        Args:
            title: Title
            snippet: Snippet

        Returns:
            List of entities
        """
        text = f'{title} {snippet}'
        entities = []
        org_suffixes = ['Inc', 'Corp', 'LLC', 'Ltd', 'Company', 'University', 'Institute']
        words = text.split()
        for i, word in enumerate(words):
            if word in org_suffixes and i > 0:
                entities.append(f'{words[i - 1]} {word}')
        import re
        date_pattern = '\\d{4}-\\d{2}-\\d{2}|\\d{1,2}/\\d{1,2}/\\d{4}|\\w+ \\d{1,2}, \\d{4}'
        dates = re.findall(date_pattern, text)
        entities.extend(dates)
        return entities[:5]

    def _extract_tags(self, title: str, snippet: str, parsed_goal=None) -> list[str]:
        """
        Extract tags from title and snippet

        Args:
            title: Title
            snippet: Snippet
            parsed_goal: Parsed task goal

        Returns:
            List of tags
        """
        tags = []
        if parsed_goal:
            if hasattr(parsed_goal, 'topic') and parsed_goal.topic:
                tags.append(parsed_goal.topic)
            if hasattr(parsed_goal, 'concept') and parsed_goal.concept:
                tags.append(parsed_goal.concept)
        text = f'{title} {snippet}'.lower()
        keywords = ['news', 'report', 'article', 'study', 'research', 'analysis', 'update', 'announcement', 'policy', 'memo', 'document']
        for keyword in keywords:
            if keyword in text:
                tags.append(keyword)
        return list(set(tags))[:10]