from lpm_kernel.L0.models import InsighterInput, SummarizerInput, FileInfo, BioInfo, DocumentType
from lpm_kernel.L0.l0_generator import L0Generator
from lpm_kernel.configs.config import Config
from lpm_kernel.file_data.document_dto import DocumentDTO
from typing import Dict, Optional

class SummaryKernel:

    def __init__(self):
        self.generator = L0Generator()
        config = Config.from_env()
        self.preferred_language = config.get('PREFER_LANGUAGE', 'en')

    def analyze(self, doc: DocumentDTO, insight: str='') -> Dict:
        """Generate document summary"""
        try:
            self.generator.preferred_language = self.preferred_language
            document_type = DocumentType.from_mime_type(doc.mime_type)
            if document_type is DocumentType.TEXT:
                return {'title': '', 'summary': doc.raw_content, 'keywords': []}
            file_info = FileInfo(data_type=document_type.value, filename=doc.name, content='', file_content={'content': doc.raw_content})
            summarizer_input = SummarizerInput(file_info=file_info, insight=insight)
            summary_result = self.generator.summarizer(summarizer_input)
            return {'title': summary_result.get('title'), 'summary': summary_result.get('summary'), 'keywords': summary_result.get('keywords', [])}
        except Exception as e:
            logger.error(f'Failed to generate summary: {str(e)}', exc_info=True)
            raise Exception(f'Error generating summary: {e}')