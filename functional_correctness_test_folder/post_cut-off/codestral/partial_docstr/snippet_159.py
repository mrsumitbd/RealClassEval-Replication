
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
        for doc in response.get('documents', []):
            formatted_doc = {
                'title': doc.get('title', ''),
                'id': doc.get('id', ''),
                'kb_id': doc.get('kb_id', ''),
                'content': doc.get('content', ''),
                'emoji': '📄'
            }
            formatted_response.append(formatted_doc)
        return formatted_response

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        '''
        Format get document response.
        Args:
            document_id: ID of the document
            kb_id: Knowledge Base ID
            content_data: Content data of the document
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_response = [{
            'title': content_data.get('title', ''),
            'id': document_id,
            'kb_id': kb_id,
            'content': content_data.get('content', ''),
            'emoji': '📄'
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
            'title': title,
            'id': doc_id,
            'kb_id': kb_id,
            'content': 'Document stored successfully',
            'emoji': '✅'
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
        emoji = '✅' if status == 'success' else '❌'
        formatted_response = [{
            'title': f'Document {doc_id}',
            'id': doc_id,
            'kb_id': kb_id,
            'content': f'Document deletion {status}',
            'emoji': emoji
        }]
        return formatted_response

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve documents response.
        Args:
            response: Raw API response from retrieve_knowledge_base_documents
            min_score: Minimum score threshold for including documents
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted_response = []
        for doc in response.get('documents', []):
            if doc.get('score', 0.0) >= min_score:
                formatted_doc = {
                    'title': doc.get('title', ''),
                    'id': doc.get('id', ''),
                    'kb_id': doc.get('kb_id', ''),
                    'content': doc.get('content', ''),
                    'score': doc.get('score', 0.0),
                    'emoji': '📄'
                }
                formatted_response.append(formatted_doc)
        return formatted_response
