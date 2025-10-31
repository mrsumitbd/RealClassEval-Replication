
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
                'type': 'document',
                'content': f"📄 **{doc.get('title', 'Untitled')}**\n"
                           f"ID: `{doc.get('id', 'N/A')}`\n"
                           f"Knowledge Base: `{doc.get('knowledge_base_id', 'N/A')}`\n"
                           f"Created: {doc.get('created_at', 'N/A')}\n"
                           f"Updated: {doc.get('updated_at', 'N/A')}"
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
        formatted = [{
            'type': 'document',
            'content': f"📄 **Document Details**\n"
                       f"ID: `{document_id}`\n"
                       f"Knowledge Base: `{kb_id}`\n"
                       f"Title: {content_data.get('title', 'N/A')}\n"
                       f"Content: {content_data.get('content', 'N/A')}"
        }]
        return formatted

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
        formatted = [{
            'type': 'success',
            'content': f"✅ **Document Stored Successfully**\n"
                       f"ID: `{doc_id}`\n"
                       f"Knowledge Base: `{kb_id}`\n"
                       f"Title: {title}"
        }]
        return formatted

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
            content = f"✅ **Document Deleted Successfully**\n"
        else:
            content = f"❌ **Failed to Delete Document**\n"

        formatted = [{
            'type': 'status',
            'content': f"{content}"
                       f"ID: `{doc_id}`\n"
                       f"Knowledge Base: `{kb_id}`"
        }]
        return formatted

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
            if result.get('score', 0) >= min_score:
                formatted.append({
                    'type': 'result',
                    'content': f"🔍 **Retrieved Document**\n"
                               f"ID: `{result.get('document_id', 'N/A')}`\n"
                               f"Knowledge Base: `{result.get('knowledge_base_id', 'N/A')}`\n"
                               f"Relevance Score: {result.get('score', 0):.2f}\n"
                               f"Content: {result.get('content', 'N/A')}"
                })
        return formatted
