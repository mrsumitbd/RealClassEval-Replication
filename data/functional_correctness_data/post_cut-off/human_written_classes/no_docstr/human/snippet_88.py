from media_manager.indexer.models import IndexerQueryResult
from media_manager.indexer.schemas import IndexerQueryResultId, IndexerQueryResult as IndexerQueryResultSchema
from sqlalchemy.orm import Session

class IndexerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_result(self, result_id: IndexerQueryResultId) -> IndexerQueryResultSchema:
        return IndexerQueryResultSchema.model_validate(self.db.get(IndexerQueryResult, result_id))

    def save_result(self, result: IndexerQueryResultSchema) -> IndexerQueryResultSchema:
        log.debug('Saving indexer query result: %s', result)
        result_data = result.model_dump()
        result_data['download_url'] = str(result.download_url)
        self.db.add(IndexerQueryResult(**result_data))
        self.db.commit()
        return result