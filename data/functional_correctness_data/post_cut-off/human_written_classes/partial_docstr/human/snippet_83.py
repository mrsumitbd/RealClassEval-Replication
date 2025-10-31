from memos.memories.textual.item import TextualMemoryItem
from datetime import datetime
from memos.embedders.factory import OllamaEmbedder
from memos.mem_reader.base import BaseMemReader
from concurrent.futures import ThreadPoolExecutor, as_completed

class XinyuSearchRetriever:
    """Xinyu Search retriever that converts search results to TextualMemoryItem format"""

    def __init__(self, access_key: str, search_engine_id: str, embedder: OllamaEmbedder, reader: BaseMemReader, max_results: int=20):
        """
        Initialize Xinyu search retriever

        Args:
            access_key: Xinyu API access key
            embedder: Embedder instance for generating embeddings
            max_results: Maximum number of results to retrieve
            reader: MemReader Moduel to deal with internet contents
        """
        self.xinyu_api = XinyuSearchAPI(access_key, search_engine_id, max_results=max_results)
        self.embedder = embedder
        self.reader = reader

    def retrieve_from_internet(self, query: str, top_k: int=10, parsed_goal=None, info=None) -> list[TextualMemoryItem]:
        """
        Retrieve information from Xinyu search and convert to TextualMemoryItem format

        Args:
            query: Search query
            top_k: Number of results to return
            parsed_goal: Parsed task goal (optional)
            info (dict): Leave a record of memory consumption.
        Returns:
            List of TextualMemoryItem
        """
        search_results = self.xinyu_api.search(query, max_results=top_k)
        memory_items: list[TextualMemoryItem] = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self._process_result, result, query, parsed_goal, info) for result in search_results]
            for future in as_completed(futures):
                try:
                    memory_items.extend(future.result())
                except Exception as e:
                    logger.error(f'Error processing search result: {e}')
        unique_memory_items = {}
        for item in memory_items:
            if item.memory not in unique_memory_items:
                unique_memory_items[item.memory] = item
        return list(unique_memory_items.values())

    def _extract_entities(self, title: str, content: str, summary: str) -> list[str]:
        """
        Extract entities from title, content and summary

        Args:
            title: Article title
            content: Article content
            summary: Article summary

        Returns:
            List of extracted entities
        """
        text = f'{title} {content} {summary}'
        entities = []
        words = text.split()
        for word in words:
            if len(word) > 2 and word[0].isupper():
                entities.append(word)
        return list(set(entities))[:10]

    def _extract_tags(self, title: str, content: str, summary: str, parsed_goal=None) -> list[str]:
        """
        Extract tags from title, content and summary

        Args:
            title: Article title
            content: Article content
            summary: Article summary
            parsed_goal: Parsed task goal (optional)

        Returns:
            List of extracted tags
        """
        tags = []
        tags.append('xinyu_search')
        tags.append('news')
        text = f'{title} {content} {summary}'.lower()
        keywords = {'economy': ['economy', 'GDP', 'growth', 'production', 'industry', 'investment', 'consumption', 'market', 'trade', 'finance'], 'politics': ['politics', 'government', 'policy', 'meeting', 'leader', 'election', 'parliament', 'ministry'], 'technology': ['technology', 'tech', 'innovation', 'digital', 'internet', 'AI', 'artificial intelligence', 'software', 'hardware'], 'sports': ['sports', 'game', 'athlete', 'olympic', 'championship', 'tournament', 'team', 'player'], 'culture': ['culture', 'education', 'art', 'history', 'literature', 'music', 'film', 'museum'], 'health': ['health', 'medical', 'pandemic', 'hospital', 'doctor', 'medicine', 'disease', 'treatment'], 'environment': ['environment', 'ecology', 'pollution', 'green', 'climate', 'sustainability', 'renewable']}
        for category, words in keywords.items():
            if any((word in text for word in words)):
                tags.append(category)
        if parsed_goal and hasattr(parsed_goal, 'tags'):
            tags.extend(parsed_goal.tags)
        return list(set(tags))[:15]

    def _process_result(self, result: dict, query: str, parsed_goal: str, info: None) -> list[TextualMemoryItem]:
        if not info:
            info = {'user_id': '', 'session_id': ''}
        title = result.get('title', '')
        content = result.get('content', '')
        summary = result.get('summary', '')
        url = result.get('url', '')
        publish_time = result.get('publish_time', '')
        if publish_time:
            try:
                publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except Exception as e:
                logger.error(f'xinyu search error: {e}')
                publish_time = datetime.now().strftime('%Y-%m-%d')
        else:
            publish_time = datetime.now().strftime('%Y-%m-%d')
        read_items = self.reader.get_memory([content], type='doc', info=info)
        memory_items = []
        for read_item_i in read_items[0]:
            read_item_i.memory = f'Title: {title}\nNewsTime: {publish_time}\nSummary: {summary}\nContent: {read_item_i.memory}'
            read_item_i.metadata.source = 'web'
            read_item_i.metadata.memory_type = 'OuterMemory'
            read_item_i.metadata.sources = [url] if url else []
            read_item_i.metadata.visibility = 'public'
            memory_items.append(read_item_i)
        return memory_items