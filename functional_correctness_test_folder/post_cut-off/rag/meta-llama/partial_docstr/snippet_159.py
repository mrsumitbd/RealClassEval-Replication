
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
        if 'data' in response and response['data']:
            for document in response['data']:
                formatted_document = {
                    'type': 'document',
                    'id': document.get('id', ''),
                    'title': document.get('title', ''),
                    'content': f"📄 {document.get('title', '')} (ID: {document.get('id', '')})"
                }
                formatted_response.append(formatted_document)
        else:
            formatted_response.append({
                'type': 'message',
                'content': '📝 No documents found in the knowledge base.'
            })
        return formatted_response

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
        formatted_response = [{
            'type': 'document_content',
            'id': document_id,
            'kb_id': kb_id,
            'content': content_data.get('content', ''),
            'metadata': content_data.get('metadata', {})
        }]
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
            'type': 'message',
            'content': f"✅ Successfully stored document '{title}' (ID: {doc_id}) in Knowledge Base {kb_id}."
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
        if status == 'success':
            formatted_response = [{
                'type': 'message',
                'content': f"🗑️ Successfully deleted document (ID: {doc_id}) from Knowledge Base {kb_id}."
            }]
        else:
            formatted_response = [{
                'type': 'error',
                'content': f"❌ Failed to delete document (ID: {doc_id}) from Knowledge Base {kb_id}."
            }]
        return formatted_response

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_response = []
        if 'data' in response and response['data']:
            for result in response['data']:
                score = result.get('score', 0.0)
                if score >= min_score:
                    formatted_result = {
                        'type': 'search_result',
                        'id': result.get('id', ''),
                        'content': result.get('content', ''),
                        'score': score,
                        'metadata': result.get('metadata', {})
                    }
                    formatted_response.append(formatted_result)
        if not formatted_response:
            formatted_response.append({
                'type': 'message',
                'content': f'🔍 No relevant results found with score >= {min_score}.'
            })
        return formatted_response
