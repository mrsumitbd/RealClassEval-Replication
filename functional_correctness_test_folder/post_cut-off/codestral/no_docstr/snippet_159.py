
class MemoryFormatter:

    def format_list_response(self, response: Dict) -> List[Dict]:
        formatted_response = []
        for kb_id, documents in response.items():
            for doc_id, title in documents.items():
                formatted_response.append({
                    "kb_id": kb_id,
                    "doc_id": doc_id,
                    "title": title
                })
        return formatted_response

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        return [{
            "kb_id": kb_id,
            "doc_id": document_id,
            "content": content_data
        }]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        return [{
            "kb_id": kb_id,
            "doc_id": doc_id,
            "title": title
        }]

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        return [{
            "kb_id": kb_id,
            "doc_id": doc_id,
            "status": status
        }]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        formatted_response = []
        for kb_id, documents in response.items():
            for doc_id, content in documents.items():
                if content["score"] >= min_score:
                    formatted_response.append({
                        "kb_id": kb_id,
                        "doc_id": doc_id,
                        "content": content["content"],
                        "score": content["score"]
                    })
        return formatted_response
