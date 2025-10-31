
from typing import Dict, List


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_response = []
        if 'documents' in response:
            for document in response['documents']:
                formatted_document = {
                    'id': document.get('id', ''),
                    'title': document.get('title', ''),
                    'content': f"📄 {document.get('title', '')}"
                }
                formatted_response.append(formatted_document)
        return formatted_response

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        formatted_response = []
        if 'content' in content_data:
            formatted_content = {
                'id': document_id,
                'kb_id': kb_id,
                'content': content_data['content']
            }
            formatted_response.append(formatted_content)
        return formatted_response

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        '''
        Format store document response.
        Args:
            doc_id: ID of the newly stored document
            kb_id: Knowledge Base ID
            title: Title of the stored document
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_response = [{
            'id': doc_id,
            'kb_id': kb_id,
            'message': f"📝 Successfully stored document '{title}' with ID {doc_id}"
        }]
        return formatted_response

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        '''
        Format delete document response.
        Args:
            status: Status of the deletion operation
            doc_id: ID of the deleted document
            kb_id: Knowledge Base ID
        Returns:
            List of formatted content dictionaries for display
        '''
        if status.lower() == 'success':
            message = f"🗑️ Successfully deleted document with ID {doc_id}"
        else:
            message = f"⚠️ Failed to delete document with ID {doc_id}"
        formatted_response = [{
            'id': doc_id,
            'kb_id': kb_id,
            'message': message
        }]
        return formatted_response

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        formatted_response = []
        if 'results' in response:
            for result in response['results']:
                if result.get('score', 0.0) >= min_score:
                    formatted_result = {
                        'id': result.get('id', ''),
                        'score': result.get('score', 0.0),
                        'content': result.get('content', ''),
                        'message': f"🔍 Retrieved relevant document with score {result.get('score', 0.0):.2f}"
                    }
                    formatted_response.append(formatted_result)
        return formatted_response
