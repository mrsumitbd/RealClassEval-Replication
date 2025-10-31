
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
        for document in response.get('documents', []):
            formatted_document = {
                'id': document['id'],
                'title': document['title'],
                'description': f"📄 {document.get('description', 'No description available')}"
            }
            formatted_response.append(formatted_document)
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
        formatted_response = []
        formatted_response.append({
            'document_id': document_id,
            'kb_id': kb_id,
            'content': content_data.get('content', 'No content available'),
            'metadata': f"📝 Metadata: {content_data.get('metadata', 'No metadata available')}"
        })
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
        formatted_response = []
        formatted_response.append({
            'status': '✅ Document stored successfully',
            'document_id': doc_id,
            'kb_id': kb_id,
            'title': title
        })
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
        formatted_response = []
        if status == 'success':
            formatted_response.append({
                'status': f'🗑️ Document {doc_id} deleted successfully from Knowledge Base {kb_id}'
            })
        else:
            formatted_response.append({
                'status': f'❌ Failed to delete document {doc_id} from Knowledge Base {kb_id}'
            })
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
        for result in response.get('results', []):
            if result['score'] >= min_score:
                formatted_result = {
                    'document_id': result['document_id'],
                    'kb_id': result['kb_id'],
                    'content': result.get('content', 'No content available'),
                    'score': f"📊 Relevance score: {result['score']:.2f}",
                    'metadata': f"📝 Metadata: {result.get('metadata', 'No metadata available')}"
                }
                formatted_response.append(formatted_result)
        return formatted_response
