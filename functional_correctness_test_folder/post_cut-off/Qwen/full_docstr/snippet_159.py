
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
        formatted_list = []
        for doc in response.get('documents', []):
            formatted_list.append({
                'Document ID': doc.get('id'),
                'Title': doc.get('title'),
                'Summary': doc.get('summary', 'No summary available'),
                'Emoji': '📜'
            })
        return formatted_list

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
            'Document ID': document_id,
            'Knowledge Base ID': kb_id,
            'Title': content_data.get('title'),
            'Content': content_data.get('content'),
            'Emoji': '📖'
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
            'Document ID': doc_id,
            'Knowledge Base ID': kb_id,
            'Title': title,
            'Status': 'Stored',
            'Emoji': '💾'
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
            'Document ID': doc_id,
            'Knowledge Base ID': kb_id,
            'Status': status,
            'Emoji': '🗑️'
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
        formatted_list = []
        for doc in response.get('documents', []):
            if doc.get('score', 0.0) >= min_score:
                formatted_list.append({
                    'Document ID': doc.get('id'),
                    'Title': doc.get('title'),
                    'Summary': doc.get('summary', 'No summary available'),
                    'Score': doc.get('score'),
                    'Emoji': '🔍'
                })
        return formatted_list
