from typing import Optional, Dict, Any
import mimetypes
import sys
import os

class FileHandler:
    """Handler for handling file operations with Docling integration."""

    def __init__(self):
        """Initialize the file handling service."""
        self.converter = None
        if DOCLING_ENABLED:
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
            from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
            from docling.document_converter import DocumentConverter, PdfFormatOption
            try:
                pipeline_options = PdfPipelineOptions()
                pipeline_options.do_ocr = True
                pipeline_options.do_table_structure = True
                pipeline_options.table_structure_options.do_cell_matching = True
                pipeline_options.ocr_options = RapidOcrOptions()
                pipeline_options.accelerator_options = AcceleratorOptions(num_threads=2, device=AcceleratorDevice.MPS)
                if sys.platform != 'darwin':
                    pipeline_options.accelerator_options = AcceleratorOptions(num_threads=4, device=AcceleratorDevice.AUTO)
                self.converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)})
                logger.info('Docling converter initialized successfully')
            except Exception as e:
                logger.error(f'Failed to initialize Docling converter: {str(e)}')

    def _guess_mime_by_extension(self, file_path: str) -> Optional[str]:
        extension = os.path.splitext(file_path)[1].lower().lstrip('.')
        if extension in EXTENSION_MIME_MAPPING:
            return EXTENSION_MIME_MAPPING[extension]
        return None

    def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file is allowed based on MIME type and size.

        Args:
            file_path: Path to the file

        Returns:
            bool: True if file is valid, False otherwise
        """
        if not os.path.exists(file_path):
            logger.warning(f'File does not exist: {file_path}')
            return False
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            logger.warning(f'File too large: {file_path} ({file_size} bytes)')
            return False
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = self._guess_mime_by_extension(file_path)
        if mime_type and mime_type not in ALLOWED_MIME_TYPES and (not mime_type.startswith('text/')):
            logger.warning(f'Unsupported MIME type: {mime_type} for {file_path}')
            return False
        return True

    def process_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a file using Docling or fallback methods.

        Args:
            file_path: Path to the file

        Returns:
            Optional[Dict[str, Any]]: Processed file content or None if processing failed
        """
        if not self.validate_file(file_path):
            return None
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = self._guess_mime_by_extension(file_path)
        if DOCLING_ENABLED and self.converter and (mime_type in DOCLING_FORMATS):
            from docling.exceptions import ConversionError
            try:
                logger.info(f'Processing file with Docling: {file_path}')
                result = self.converter.convert(file_path)
                markdown_content = result.document.export_to_markdown()
                return {'type': 'text', 'text': f'Content of {file_path} (converted to Markdown):\n\n{markdown_content}'}
            except ConversionError as e:
                logger.warning(f'Docling conversion failed for {file_path}: {str(e)}')
            except Exception as e:
                logger.error(f'Unexpected error in Docling conversion: {str(e)}')
        elif mime_type and mime_type.startswith('text/'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {'type': 'text', 'text': f'Content of {file_path}:\n\n{content}'}
            except Exception as e:
                logger.error(f'Error reading text file {file_path}: {str(e)}')
                return None
        return None