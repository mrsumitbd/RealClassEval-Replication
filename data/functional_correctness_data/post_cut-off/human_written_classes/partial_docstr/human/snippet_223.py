from typing import Any, Dict, List, Optional

class VectorDBBackend:
    """
    Abstract vector DB interface for pluggable backends.
    """

    def add(self, embeddings: List[List[float]], metadatas: List[Dict[str, Any]], ids: Optional[List[str]]=None):
        raise NotImplementedError

    def query(self, embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def persist(self):
        pass

    def delete(self, ids: List[str]):
        """Remove vectors by their IDs. Backends that don't support fine-grained deletes may no-op."""
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError