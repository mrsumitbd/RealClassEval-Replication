
from typing import Dict, List


class MemoryFormatter:

    def format_list_response(self, response: Dict) -> List[Dict]:
        return [{"document_id": doc["id"], "title": doc["title"]} for doc in response.get("documents", [])]

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        return [{"document_id": document_id, "kb_id": kb_id, "content": content_data.get("content", "")}]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        return [{"document_id": doc_id, "kb_id": kb_id, "title": title, "status": "stored"}]

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        return [{"document_id": doc_id, "kb_id": kb_id, "status": status}]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        return [{"document_id": doc["id"], "score": doc["score"], "content": doc["content"]} for doc in response.get("documents", []) if doc["score"] >= min_score]
