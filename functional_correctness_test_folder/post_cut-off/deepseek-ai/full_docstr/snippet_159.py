
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
        formatted_docs = []
        if 'documents' in response:
            for doc in response['documents']:
                formatted_doc = {
                    'id': doc.get('id', 'N/A'),
                    'title': doc.get('title', 'Untitled'),
                    'kb_id': doc.get('kb_id', 'N/A'),
                    'status': doc.get('status', 'N/A'),
                    'created_at': doc.get('created_at', 'N/A'),
                    'updated_at': doc.get('updated_at', 'N/A')
                }
                formatted_docs.append(formatted_doc)
        return formatted_docs

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        '''
        Format get document response.
        Args:
            document_id: ID of the retrieved document
            kb_id: Knowledge Base ID
            content_data: Parsed content data from the document
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_content = {
            'id': document_id,
            'kb_id': kb_id,
            'content': content_data.get('content', 'No content available'),
            'metadata': content_data.get('metadata', {})
        }
        return [formatted_content]

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
        return [{
            'id': doc_id,
            'kb_id': kb_id,
            'title': title,
            'status': 'stored',
            'message': 'Document successfully stored'
        }]

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
        return [{
            'id': doc_id,
            'kb_id': kb_id,
            'status': status,
            'message': f'Document deletion {status}'
        }]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_results = []
        if 'results' in response:
            for result in response['results']:
                if result.get('score', 0.0) >= min_score:
                    formatted_result = {
                        'id': result.get('id', 'N/A'),
                        'kb_id': result.get('kb_id', 'N/A'),
                        'content': result.get('content', 'No content available'),
                        'score': result.get('score', 0.0),
                        'metadata': result.get('metadata', {})
                    }
                    formatted_results.append(formatted_result)
        return formatted_results
