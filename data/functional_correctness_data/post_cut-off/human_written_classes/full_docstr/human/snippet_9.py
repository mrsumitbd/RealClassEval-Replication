from lpm_kernel.kernel.l1.l1_manager import get_latest_global_bio
from lpm_kernel.file_data.embedding_service import EmbeddingService, ChunkDTO

class L1KnowledgeRetriever:
    """L1 knowledge retriever"""

    def __init__(self, embedding_service: EmbeddingService, similarity_threshold: float=0.7, max_shades: int=3):
        """
        init L1 knowledge retriever

        Args:
            embedding_service: Embedding service instance
            similarity_threshold: only return contents whose similarity bigger than this value
            max_shades: the maximum number of return shades
        """
        self.embedding_service = embedding_service
        self.similarity_threshold = similarity_threshold
        self.max_shades = max_shades

    def retrieve(self, query: str) -> str:
        """
        search related L1 shades

        Args:
            query: query content

        Returns:
            str: structured knowledge content, or empty string if no relevant knowledge found
        """
        try:
            global_bio = get_latest_global_bio()
            if not global_bio or not global_bio.shades:
                logger.info('Global Bio not found or Shades is empty')
                return ''
            query_embedding = self.embedding_service.get_embedding(query)
            if not query_embedding:
                logger.error('Failed to get embedding for query text')
                return ''
            shade_embeddings = []
            for shade in global_bio.shades:
                shade_text = f"{shade.get('title', '')} - {shade.get('description', '')}"
                embedding = self.embedding_service.get_embedding(shade_text)
                if embedding:
                    shade_embeddings.append((shade, embedding))
            if not shade_embeddings:
                logger.info('No available Shades embeddings found')
                return ''
            similar_shades = []
            for shade, embedding in shade_embeddings:
                similarity = self.embedding_service.calculate_similarity(query_embedding, embedding)
                if similarity >= self.similarity_threshold:
                    similar_shades.append((shade, similarity))
            similar_shades.sort(key=lambda x: x[1], reverse=True)
            similar_shades = similar_shades[:self.max_shades]
            if not similar_shades:
                return ''
            shade_parts = []
            for shade, similarity in similar_shades:
                shade_text = f"Shade: {shade.get('title', '')}\n"
                shade_text += f"Description: {shade.get('description', '')}\n"
                shade_text += f'Similarity: {similarity:.2f}'
                shade_parts.append(shade_text)
            return '\n\n'.join(shade_parts)
        except Exception as e:
            logger.error(f'L1 knowledge retrieval failed: {str(e)}')
            return ''