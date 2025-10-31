from typing import Any, Dict, List, Optional
import json

class MemoryFormatter:
    """
    Formats memory tool responses for display.

    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    """

    def format_list_response(self, response: Dict) -> List[Dict]:
        """
        Format list documents response.

        Args:
            response: Raw API response from list_knowledge_base_documents

        Returns:
            List of formatted content dictionaries for display
        """
        content = []
        document_details = response.get('documentDetails', [])
        if not document_details:
            content.append({'text': 'No documents found.'})
            return content
        result_text = f'Found {len(document_details)} documents:'
        for i, doc in enumerate(document_details, 1):
            doc_id = None
            if doc.get('identifier') and doc['identifier'].get('custom'):
                doc_id = doc['identifier']['custom'].get('id')
            elif doc.get('identifier') and doc['identifier'].get('s3'):
                doc_id = doc['identifier']['s3'].get('uri')
            if doc_id:
                status = doc.get('status', 'UNKNOWN')
                updated_at = doc.get('updatedAt', 'Unknown')
                result_text += f'\n{i}. 🔖 ID: {doc_id}'
                result_text += f'\n   📊 Status: {status}'
                result_text += f'\n   🕒 Updated: {updated_at}'
        content.append({'text': result_text})
        if 'nextToken' in response:
            content.append({'text': '➡️ More results available. Use next_token parameter to continue.'})
            content.append({'text': f"next_token: {response['nextToken']}"})
        return content

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        """
        Format get document response.

        Args:
            document_id: ID of the retrieved document
            kb_id: Knowledge Base ID
            content_data: Parsed content data from the document

        Returns:
            List of formatted content dictionaries for display
        """
        result = [{'text': '✅ Document retrieved successfully:'}, {'text': f"📝 Title: {content_data.get('title', 'Unknown')}"}, {'text': f'🔑 Document ID: {document_id}'}, {'text': f'🗄️ Knowledge Base ID: {kb_id}'}, {'text': f"\n📄 Content:\n\n{content_data.get('content', 'No content available')}"}]
        return result

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        """
        Format store document response.

        Args:
            doc_id: ID of the newly stored document
            kb_id: Knowledge Base ID
            title: Title of the stored document

        Returns:
            List of formatted content dictionaries for display
        """
        content = [{'text': '✅ Successfully stored content in knowledge base:'}, {'text': f'📝 Title: {title}'}, {'text': f'🔑 Document ID: {doc_id}'}, {'text': f'🗄️ Knowledge Base ID: {kb_id}'}]
        return content

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        """
        Format delete document response.

        Args:
            status: Status of the deletion operation
            doc_id: ID of the deleted document
            kb_id: Knowledge Base ID

        Returns:
            List of formatted content dictionaries for display
        """
        if status in ['DELETED', 'DELETING', 'DELETE_IN_PROGRESS']:
            content = [{'text': f"✅ Document deletion {status.lower().replace('_', ' ')}:"}, {'text': f'🔑 Document ID: {doc_id}'}, {'text': f'🗄️ Knowledge Base ID: {kb_id}'}]
        else:
            content = [{'text': f'❌ Document deletion failed with status: {status}'}, {'text': f'🔑 Document ID: {doc_id}'}, {'text': f'🗄️ Knowledge Base ID: {kb_id}'}]
        return content

    def format_retrieve_response(self, response: Dict, min_score: float=0.0) -> List[Dict]:
        """
        Format retrieve response.

        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results

        Returns:
            List of formatted content dictionaries for display
        """
        content = []
        results = response.get('retrievalResults', [])
        filtered_results = [r for r in results if r.get('score', 0) >= min_score]
        if not filtered_results:
            content.append({'text': 'No results found that meet the score threshold.'})
            return content
        result_text = f'Retrieved {len(filtered_results)} results with score >= {min_score}:'
        for result in filtered_results:
            score = result.get('score', 0)
            doc_id = 'unknown'
            text = 'No content available'
            title = None
            if 'location' in result and 'customDocumentLocation' in result['location']:
                doc_id = result['location']['customDocumentLocation'].get('id', 'unknown')
            if 'content' in result and 'text' in result['content']:
                text = result['content']['text']
            result_text += f'\n\nScore: {score:.4f}'
            result_text += f'\nDocument ID: {doc_id}'
            try:
                if text.strip().startswith('{'):
                    content_obj = json.loads(text)
                    if isinstance(content_obj, dict) and 'title' in content_obj:
                        title = content_obj.get('title')
                        result_text += f'\nTitle: {title}'
            except json.JSONDecodeError:
                pass
            preview = text[:150]
            if len(text) > 150:
                preview += '...'
            result_text += f'\nContent Preview: {preview}'
        content.append({'text': result_text})
        if 'nextToken' in response:
            content.append({'text': '\n➡️ More results available. Use next_token parameter to continue.'})
            content.append({'text': f"next_token: {response['nextToken']}"})
        return content