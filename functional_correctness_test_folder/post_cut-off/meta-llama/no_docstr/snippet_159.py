
from typing import Dict, List


class MemoryFormatter:

    def format_list_response(self, response: Dict) -> List[Dict]:
        """Format the response from listing documents in the knowledge base."""
        formatted_response = []
        for item in response.get('items', []):
            formatted_response.append({
                'id': item.get('id'),
                'title': item.get('title')
            })
        return formatted_response

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        """Format the response from getting a document from the knowledge base."""
        formatted_response = [{
            'document_id': document_id,
            'kb_id': kb_id,
            'content': content_data.get('content'),
            'metadata': content_data.get('metadata', {})
        }]
        return formatted_response

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        """Format the response from storing a document in the knowledge base."""
        formatted_response = [{
            'document_id': doc_id,
            'kb_id': kb_id,
            'title': title
        }]
        return formatted_response

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        """Format the response from deleting a document from the knowledge base."""
        formatted_response = [{
            'status': status,
            'document_id': doc_id,
            'kb_id': kb_id
        }]
        return formatted_response

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        """Format the response from retrieving documents from the knowledge base."""
        formatted_response = []
        for result in response.get('results', []):
            if result.get('score', 0.0) >= min_score:
                formatted_response.append({
                    'document_id': result.get('id'),
                    'score': result.get('score'),
                    'metadata': result.get('metadata', {}),
                    'content': result.get('content')
                })
        return formatted_response
