
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
        formatted = []
        for doc in response.get('documents', []):
            formatted.append({
                'title': f"📄 {doc.get('title', 'Untitled')}",
                'id': doc.get('id', ''),
                'kb_id': doc.get('kb_id', ''),
                'metadata': doc.get('metadata', {})
            })
        return formatted

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
        return [{
            'title': f"📖 {content_data.get('title', 'Untitled')}",
            'content': content_data.get('content', ''),
            'id': document_id,
            'kb_id': kb_id,
            'metadata': content_data.get('metadata', {})
        }]

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
            'title': f"✅ Stored: {title}",
            'id': doc_id,
            'kb_id': kb_id,
            'status': 'success'
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
        emoji = '✅' if status == 'success' else '❌'
        return [{
            'title': f"{emoji} Deleted document {doc_id}",
            'id': doc_id,
            'kb_id': kb_id,
            'status': status
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
        formatted = []
        for result in response.get('results', []):
            if result.get('score', 0.0) >= min_score:
                formatted.append({
                    'title': f"🔍 {result.get('title', 'Untitled')} (Score: {result.get('score', 0.0):.2f})",
                    'content': result.get('content', ''),
                    'id': result.get('id', ''),
                    'kb_id': result.get('kb_id', ''),
                    'metadata': result.get('metadata', {})
                })
        return formatted
