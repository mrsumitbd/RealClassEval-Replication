from lpm_kernel.models.l1 import L1Version, L1ChunkTopic
from lpm_kernel.file_data.document_repository import DocumentRepository
from lpm_kernel.L1.bio import Chunk
from lpm_kernel.file_data.models import ChunkModel
from lpm_kernel.common.repository.database_session import DatabaseSession

class ChunkService:

    def __init__(self):
        self._repository = DocumentRepository()

    def query_topics_data(self) -> dict[str, dict]:
        topics_data = {}
        with DatabaseSession.session() as session:
            latest_version = session.query(L1Version).order_by(L1Version.version.desc()).first()
            if not latest_version:
                return {}
            chunk_topics = session.query(L1ChunkTopic).filter(L1ChunkTopic.version == latest_version.version).all()
            if not chunk_topics:
                return {}
            for i, topic in enumerate(chunk_topics):
                topics_data[str(i)] = {'indices': [i], 'docIds': [i], 'contents': [topic.topic] if topic.topic else [], 'chunkIds': [topic.chunk_id] if topic.chunk_id else [], 'tags': topic.tags if topic.tags else [], 'topic': topic.topic if topic.topic else '', 'topicId': i, 'recTimes': 0}
            return topics_data

    def save_chunk(self, chunk: Chunk) -> None:
        """
        Save document chunk to database
        Args:
            chunk (Chunk): Chunk object to save
        Raises:
            Exception: Error when saving fails
        """
        try:
            chunk_model = ChunkModel(document_id=chunk.document_id, content=chunk.content, tags=chunk.tags, topic=chunk.topic)
            self._repository.save_chunk(chunk_model)
            logger.debug(f'Saved chunk for document {chunk.document_id}')
        except Exception as e:
            logger.error(f'Error saving chunk: {str(e)}')
            raise