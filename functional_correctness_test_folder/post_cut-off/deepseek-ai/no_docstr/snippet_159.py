
from typing import Dict, List


class MemoryFormatter:

    def format_list_response(self, response: Dict) -> List[Dict]:
        formatted_response = []
        if "documents" in response:
            for doc in response["documents"]:
                formatted_doc = {
                    "id": doc.get("id", ""),
                    "kb_id": doc.get("kb_id", ""),
                    "title": doc.get("title", ""),
                    "created_at": doc.get("created_at", ""),
                    "updated_at": doc.get("updated_at", "")
                }
                formatted_response.append(formatted_doc)
        return formatted_response

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        formatted_response = [{
            "id": document_id,
            "kb_id": kb_id,
            "content": content_data.get("content", ""),
            "metadata": content_data.get("metadata", {})
        }]
        return formatted_response

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        formatted_response = [{
            "id": doc_id,
            "kb_id": kb_id,
            "title": title,
            "status": "stored"
        }]
        return formatted_response

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        formatted_response = [{
            "id": doc_id,
            "kb_id": kb_id,
            "status": status
        }]
        return formatted_response

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        formatted_response = []
        if "matches" in response:
            for match in response["matches"]:
                if match.get("score", 0.0) >= min_score:
                    formatted_match = {
                        "id": match.get("id", ""),
                        "kb_id": match.get("kb_id", ""),
                        "content": match.get("content", ""),
                        "metadata": match.get("metadata", {}),
                        "score": match.get("score", 0.0)
                    }
                    formatted_response.append(formatted_match)
        return formatted_response
