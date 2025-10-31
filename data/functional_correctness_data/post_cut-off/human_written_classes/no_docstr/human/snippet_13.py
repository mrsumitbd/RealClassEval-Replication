from lpm_kernel.L1.bio import Note
from lpm_kernel.common.repository.database_session import DatabaseSession
from lpm_kernel.models.l1 import L1Version, L1ChunkTopic
from lpm_kernel.file_data.document_repository import DocumentRepository
from typing import List

class NoteService:

    def __init__(self):
        self._repository = DocumentRepository()

    def prepareNotes(self, notes_list: List[Note]):
        with DatabaseSession.session() as session:
            latest_version = session.query(L1Version).order_by(L1Version.version.desc()).first()
            if latest_version:
                chunk_topics = session.query(L1ChunkTopic).filter(L1ChunkTopic.version == latest_version.version).all()
                topic_map = {str(topic.chunk_id): {'topic': topic.topic, 'tags': topic.tags} for topic in chunk_topics}
                for note in notes_list:
                    for chunk in note.chunks:
                        if str(chunk.id) in topic_map:
                            chunk.topic = topic_map[str(chunk.id)]['topic']
                            chunk.tags = topic_map[str(chunk.id)]['tags']