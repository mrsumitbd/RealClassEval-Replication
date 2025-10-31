import datetime
from typing import List, Dict, Any
from pytidb.datatype import TEXT
from pytidb.schema import TableModel, Field, Column

class Memory:

    def __init__(self, tidb_client, embedding_fn, openai_client):
        self.tidb_client = tidb_client
        self.embedding_fn = embedding_fn
        self.openai_client = openai_client

        class MemoryRecord(TableModel):
            __tablename__ = 'memories'
            __table_args__ = {'extend_existing': True}
            id: int = Field(default=None, primary_key=True)
            user_id: str
            memory: str = Field(sa_column=Column(TEXT))
            embedding: List[float] = embedding_fn.VectorField(source_field='memory')
            created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
        self.MemoryRecord = MemoryRecord
        self.table = tidb_client.create_table(schema=MemoryRecord, if_exists='skip')

    def add(self, messages: List[Dict[str, Any]], user_id: str='default_user'):
        """Add a new memory by extracting key facts from conversation."""
        prompt = 'Extract the key facts from the following conversation. Only return the facts as a single string, do not include any explanation or formatting.\n\n'
        for m in messages:
            prompt += f"{m['role']}: {m['content']}\n"
        response = self.openai_client.chat.completions.create(model='gpt-4o', messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': prompt}])
        facts = response.choices[0].message.content.strip()
        record = self.MemoryRecord(user_id=user_id, memory=facts)
        self.table.insert(record)

    def search(self, query: str, user_id: str='default_user', limit: int=3) -> Dict[str, Any]:
        """Search for relevant memories using vector similarity."""
        results = self.table.search(query=query, search_type='vector').filter({'user_id': user_id}).limit(limit).to_list()
        return {'results': results}

    def get_all_memories(self, user_id: str='default_user') -> List[Dict]:
        """Get all memories for a user, ordered by creation date."""
        results = self.table.query(filters={'user_id': user_id}, order_by={'created_at': 'desc'})
        return results.to_list()