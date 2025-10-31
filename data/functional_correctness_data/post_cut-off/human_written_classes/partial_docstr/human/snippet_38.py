from typing import List, Dict, Optional, Any
import re
from datetime import datetime
import os
from urllib.parse import urlparse, unquote

class DoclingConverter:
    """文档转换器，使用docling将文档转换为Markdown格式，支持图片提取"""

    def __init__(self):
        if not DOCLING_AVAILABLE:
            raise ImportError('docling package is not available. Please install it first.')
        pdf_pipeline_options = PdfPipelineOptions()
        pdf_pipeline_options.do_ocr = False
        pdf_pipeline_options.do_table_structure = False
        try:
            self.converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options)})
        except Exception:
            self.converter = DocumentConverter()

    def is_supported_format(self, file_path: str) -> bool:
        """检查文件格式是否支持转换"""
        if not DOCLING_AVAILABLE:
            return False
        supported_extensions = {'.pdf', '.docx', '.pptx', '.html', '.md', '.txt'}
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in supported_extensions

    def is_url(self, path: str) -> bool:
        """检查路径是否为URL"""
        try:
            result = urlparse(path)
            return result.scheme in ('http', 'https')
        except Exception:
            return False

    def extract_images(self, doc, output_dir: str) -> Dict[str, str]:
        """
        提取文档中的图片并保存到本地

        Args:
            doc: docling文档对象
            output_dir: 输出目录

        Returns:
            图片ID到本地文件路径的映射
        """
        images_dir = os.path.join(output_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        image_map = {}
        try:
            images = getattr(doc, 'images', [])
            for idx, img in enumerate(images):
                try:
                    ext = getattr(img, 'format', None) or 'png'
                    if ext.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']:
                        ext = 'png'
                    filename = f'image_{idx + 1}.{ext}'
                    filepath = os.path.join(images_dir, filename)
                    img_data = getattr(img, 'data', None)
                    if img_data:
                        with open(filepath, 'wb') as f:
                            f.write(img_data)
                        rel_path = os.path.relpath(filepath, output_dir)
                        img_id = getattr(img, 'id', str(idx + 1))
                        image_map[img_id] = rel_path
                except Exception as img_error:
                    print(f'Warning: Failed to extract image {idx + 1}: {img_error}')
                    continue
        except Exception as e:
            print(f'Warning: Failed to extract images: {e}')
        return image_map

    def process_markdown_with_images(self, markdown_content: str, image_map: Dict[str, str]) -> str:
        """
        处理Markdown内容，替换图片占位符为实际的图片路径

        Args:
            markdown_content: 原始Markdown内容
            image_map: 图片ID到本地路径的映射

        Returns:
            处理后的Markdown内容
        """

        def replace_img(match):
            img_id = match.group(1)
            if img_id in image_map:
                return f'![Image]({image_map[img_id]})'
            else:
                return match.group(0)
        processed_content = re.sub('!\\[Image\\]\\(docling://image/([^)]+)\\)', replace_img, markdown_content)
        return processed_content

    def convert_to_markdown(self, input_file: str, output_file: Optional[str]=None, extract_images: bool=True) -> Dict[str, Any]:
        """
        将文档转换为Markdown格式，支持图片提取

        Args:
            input_file: 输入文件路径或URL
            output_file: 输出Markdown文件路径（可选）
            extract_images: 是否提取图片（默认True）

        Returns:
            转换结果字典
        """
        if not DOCLING_AVAILABLE:
            return {'success': False, 'error': 'docling package is not available'}
        try:
            if not self.is_url(input_file):
                if not os.path.exists(input_file):
                    return {'success': False, 'error': f'Input file not found: {input_file}'}
                if not self.is_supported_format(input_file):
                    return {'success': False, 'error': f'Unsupported file format: {os.path.splitext(input_file)[1]}'}
            elif not input_file.lower().endswith(('.pdf', '.docx', '.pptx', '.html', '.md', '.txt')):
                return {'success': False, 'error': f'Unsupported URL format: {input_file}'}
            if not output_file:
                if self.is_url(input_file):
                    filename = URLExtractor.infer_filename_from_url(input_file)
                    base_name = os.path.splitext(filename)[0]
                else:
                    base_name = os.path.splitext(input_file)[0]
                output_file = f'{base_name}.md'
            output_dir = os.path.dirname(output_file) or '.'
            os.makedirs(output_dir, exist_ok=True)
            start_time = datetime.now()
            result = self.converter.convert(input_file)
            doc = result.document
            image_map = {}
            images_extracted = 0
            if extract_images:
                image_map = self.extract_images(doc, output_dir)
                images_extracted = len(image_map)
            markdown_content = doc.export_to_markdown()
            if extract_images and image_map:
                markdown_content = self.process_markdown_with_images(markdown_content, image_map)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            duration = (datetime.now() - start_time).total_seconds()
            if self.is_url(input_file):
                input_size = 0
            else:
                input_size = os.path.getsize(input_file)
            output_size = os.path.getsize(output_file)
            return {'success': True, 'input_file': input_file, 'output_file': output_file, 'input_size': input_size, 'output_size': output_size, 'duration': duration, 'markdown_content': markdown_content, 'images_extracted': images_extracted, 'image_map': image_map}
        except Exception as e:
            return {'success': False, 'input_file': input_file, 'error': f'Conversion failed: {str(e)}'}