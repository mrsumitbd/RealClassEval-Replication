from typing import Dict, Optional
from lpm_kernel.file_data.document_dto import DocumentDTO
from lpm_kernel.L0.l0_generator import L0Generator
from lpm_kernel.configs.config import Config
from lpm_kernel.L0.models import InsighterInput, SummarizerInput, FileInfo, BioInfo, DocumentType

class InsightKernel:

    def __init__(self):
        self.generator = L0Generator()
        config = Config.from_env()
        self.preferred_language = config.get('PREFER_LANGUAGE', 'en')

    def analyze(self, doc: DocumentDTO) -> Dict:
        """Generate document insight"""
        try:
            self.generator.preferred_language = self.preferred_language
            document_type = DocumentType.from_mime_type(doc.mime_type)
            if document_type is DocumentType.TEXT:
                return {'title': '', 'insight': doc.raw_content}
            file_info = FileInfo(data_type=document_type.value, filename=doc.name, content='', file_content={'content': doc.raw_content})
            bio_info = BioInfo(global_bio='', status_bio='', about_me='')
            insighter_input = InsighterInput(file_info=file_info, bio_info=bio_info)
            insight_result = self.generator.insighter(insighter_input)
            return {'title': insight_result.get('title'), 'insight': insight_result.get('insight')}
        except Exception as e:
            logger.error(f'Failed to generate insight: {str(e)}', exc_info=True)
            raise Exception(f'Error generating insight: {e}')