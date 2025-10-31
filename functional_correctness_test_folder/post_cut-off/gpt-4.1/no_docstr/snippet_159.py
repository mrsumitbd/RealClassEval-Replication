
from typing import Dict, List


class MemoryFormatter:

    def format_list_response(self, response: Dict) -> List[Dict]:
        documents = response.get("documents", [])
        kb_id = response.get("kb_id", "")
        result = []
        for doc in documents:
            result.append({
                "document_id": doc.get("id", ""),
                "kb_id": kb_id,
                "title": doc.get("title", ""),
                "metadata": doc.get("metadata", {})
            })
        return result

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        return [{
            "document_id": document_id,
            "kb_id": kb_id,
            "title": content_data.get("title", ""),
            "content": content_data.get("content", ""),
            "metadata": content_data.get("metadata", {})
        }]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        return [{
            "document_id": doc_id,
            "kb_id": kb_id,
            "title": title,
            "status": "stored"
        }]

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        return [{
            "document_id": doc_id,
            "kb_id": kb_id,
            "status": status
        }]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        results = []
        for item in response.get("results", []):
            score = item.get("score", 0.0)
            if score >= min_score:
                results.append({
                    "document_id": item.get("document_id", ""),
                    "kb_id": item.get("kb_id", ""),
                    "content": item.get("content", ""),
                    "score": score,
                    "metadata": item.get("metadata", {})
                })
        return results
