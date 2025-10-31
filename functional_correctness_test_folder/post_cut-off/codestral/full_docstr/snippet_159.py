
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
                'type': 'document',
                'content': f"📄 {doc.get('title', 'Untitled')}",
                'metadata': {
                    'id': doc.get('id'),
                    'kb_id': doc.get('kb_id'),
                    'created_at': doc.get('created_at')
                }
            }
            formatted_response.append(formatted_doc)
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
            'type': 'document',
            'content': f"📄 {content_data.get('title', 'Untitled')}",
            'metadata': {
                'id': document_id,
                'kb_id': kb_id,
                'created_at': content_data.get('created_at')
            },
            'sections': []
        }]

        for section in content_data.get('sections', []):
            formatted_section = {
                'type': 'section',
                'content': section.get('content', ''),
                'metadata': {
                    'section_id': section.get('id')
                }
            }
            formatted_response[0]['sections'].append(formatted_section)

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
        return [{
            'type': 'document',
            'content': f"📄 {title} has been successfully stored!",
            'metadata': {
                'id': doc_id,
                'kb_id': kb_id
            }
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
            'type': 'document',
            'content': f"{emoji} Document {doc_id} has been {status}fully deleted.",
            'metadata': {
                'id': doc_id,
                'kb_id': kb_id,
                'status': status
            }
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
        formatted_response = []
        for result in response.get('results', []):
            if result.get('score', 0.0) >= min_score:
                formatted_result = {
                    'type': 'result',
                    'content': result.get('content', ''),
                    'metadata': {
                        'id': result.get('id'),
                        'kb_id': result.get('kb_id'),
                        'score': result.get('score'),
                        'title': result.get('title')
                    }
                }
                formatted_response.append(formatted_result)
        return formatted_response
