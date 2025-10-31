import platform
import logging
import tempfile
import shutil
import subprocess
from typing import Union, Optional, Dict, Any
from pathlib import Path

class PDFConverter:
    """
    PDF conversion utility class.

    Provides methods to convert Office documents and text files to PDF format.
    """
    OFFICE_FORMATS = {'.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'}
    TEXT_FORMATS = {'.txt', '.md'}
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        """Initialize the PDF converter."""
        pass

    @staticmethod
    def convert_office_to_pdf(doc_path: Union[str, Path], output_dir: Optional[str]=None) -> Path:
        """
        Convert Office document (.doc, .docx, .ppt, .pptx, .xls, .xlsx) to PDF.
        Requires LibreOffice to be installed.

        Args:
            doc_path: Path to the Office document file
            output_dir: Output directory for the PDF file

        Returns:
            Path to the generated PDF file
        """
        try:
            doc_path = Path(doc_path)
            if not doc_path.exists():
                raise FileNotFoundError(f'Office document does not exist: {doc_path}')
            name_without_suff = doc_path.stem
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = doc_path.parent / 'pdf_output'
            base_output_dir.mkdir(parents=True, exist_ok=True)
            libreoffice_available = False
            working_libreoffice_cmd: Optional[str] = None
            subprocess_kwargs: Dict[str, Any] = {'capture_output': True, 'check': True, 'timeout': 10, 'encoding': 'utf-8', 'errors': 'ignore'}
            if platform.system() == 'Windows':
                subprocess_kwargs['creationflags'] = 134217728
            try:
                result = subprocess.run(['libreoffice', '--version'], **subprocess_kwargs)
                libreoffice_available = True
                working_libreoffice_cmd = 'libreoffice'
                logging.info(f'LibreOffice detected: {result.stdout.strip()}')
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass
            if not libreoffice_available:
                for cmd in ['soffice', 'libreoffice']:
                    try:
                        result = subprocess.run([cmd, '--version'], **subprocess_kwargs)
                        libreoffice_available = True
                        working_libreoffice_cmd = cmd
                        logging.info(f"LibreOffice detected with command '{cmd}': {result.stdout.strip()}")
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                        continue
            if not libreoffice_available:
                raise RuntimeError('LibreOffice is required for Office document conversion but was not found.\nPlease install LibreOffice:\n- Windows: Download from https://www.libreoffice.org/download/download/\n- macOS: brew install --cask libreoffice\n- Ubuntu/Debian: sudo apt-get install libreoffice\n- CentOS/RHEL: sudo yum install libreoffice\nAlternatively, convert the document to PDF manually.')
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                logging.info(f'Converting {doc_path.name} to PDF using LibreOffice...')
                commands_to_try = [working_libreoffice_cmd]
                if working_libreoffice_cmd == 'libreoffice':
                    commands_to_try.append('soffice')
                else:
                    commands_to_try.append('libreoffice')
                conversion_successful = False
                for cmd in commands_to_try:
                    if cmd is None:
                        continue
                    try:
                        convert_cmd = [cmd, '--headless', '--convert-to', 'pdf', '--outdir', str(temp_path), str(doc_path)]
                        convert_subprocess_kwargs: Dict[str, Any] = {'capture_output': True, 'text': True, 'timeout': 60, 'encoding': 'utf-8', 'errors': 'ignore'}
                        if platform.system() == 'Windows':
                            convert_subprocess_kwargs['creationflags'] = 134217728
                        result = subprocess.run(convert_cmd, **convert_subprocess_kwargs)
                        if result.returncode == 0:
                            conversion_successful = True
                            logging.info(f'Successfully converted {doc_path.name} to PDF')
                            break
                        else:
                            logging.warning(f"LibreOffice command '{cmd}' failed: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        logging.warning(f"LibreOffice command '{cmd}' timed out")
                    except Exception as e:
                        logging.error(f"LibreOffice command '{cmd}' failed with exception: {e}")
                if not conversion_successful:
                    raise RuntimeError(f'LibreOffice conversion failed for {doc_path.name}. Please check if the file is corrupted or try converting manually.')
                pdf_files = list(temp_path.glob('*.pdf'))
                if not pdf_files:
                    raise RuntimeError(f'PDF conversion failed for {doc_path.name} - no PDF file generated. Please check LibreOffice installation or try manual conversion.')
                pdf_path = pdf_files[0]
                logging.info(f'Generated PDF: {pdf_path.name} ({pdf_path.stat().st_size} bytes)')
                if pdf_path.stat().st_size < 100:
                    raise RuntimeError('Generated PDF appears to be empty or corrupted. Original file may have issues or LibreOffice conversion failed.')
                final_pdf_path = base_output_dir / f'{name_without_suff}.pdf'
                shutil.copy2(pdf_path, final_pdf_path)
                return final_pdf_path
        except Exception as e:
            logging.error(f'Error in convert_office_to_pdf: {str(e)}')
            raise

    @staticmethod
    def convert_text_to_pdf(text_path: Union[str, Path], output_dir: Optional[str]=None) -> Path:
        """
        Convert text file (.txt, .md) to PDF using ReportLab with full markdown support.

        Args:
            text_path: Path to the text file
            output_dir: Output directory for the PDF file

        Returns:
            Path to the generated PDF file
        """
        try:
            text_path = Path(text_path)
            if not text_path.exists():
                raise FileNotFoundError(f'Text file does not exist: {text_path}')
            supported_text_formats = {'.txt', '.md'}
            if text_path.suffix.lower() not in supported_text_formats:
                raise ValueError(f'Unsupported text format: {text_path.suffix}')
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            except UnicodeDecodeError:
                for encoding in ['gbk', 'latin-1', 'cp1252']:
                    try:
                        with open(text_path, 'r', encoding=encoding) as f:
                            text_content = f.read()
                        logging.info(f'Successfully read file with {encoding} encoding')
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise RuntimeError(f'Could not decode text file {text_path.name} with any supported encoding')
            if output_dir:
                base_output_dir = Path(output_dir)
            else:
                base_output_dir = text_path.parent / 'pdf_output'
            base_output_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = base_output_dir / f'{text_path.stem}.pdf'
            logging.info(f'Converting {text_path.name} to PDF...')
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.pdfbase import pdfmetrics
                doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)
                styles = getSampleStyleSheet()
                normal_style = styles['Normal']
                heading_style = styles['Heading1']
                try:
                    system = platform.system()
                    if system == 'Windows':
                        for font_name in ['SimSun', 'SimHei', 'Microsoft YaHei']:
                            try:
                                from reportlab.pdfbase.cidfonts import UnicodeCIDFont
                                pdfmetrics.registerFont(UnicodeCIDFont(font_name))
                                normal_style.fontName = font_name
                                heading_style.fontName = font_name
                                break
                            except Exception:
                                continue
                    elif system == 'Darwin':
                        for font_name in ['STSong-Light', 'STHeiti']:
                            try:
                                from reportlab.pdfbase.cidfonts import UnicodeCIDFont
                                pdfmetrics.registerFont(UnicodeCIDFont(font_name))
                                normal_style.fontName = font_name
                                heading_style.fontName = font_name
                                break
                            except Exception:
                                continue
                except Exception:
                    pass
                story = []
                if text_path.suffix.lower() == '.md':
                    lines = text_content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            story.append(Spacer(1, 12))
                            continue
                        if line.startswith('#'):
                            level = len(line) - len(line.lstrip('#'))
                            header_text = line.lstrip('#').strip()
                            if header_text:
                                header_style = ParagraphStyle(name=f'Heading{level}', parent=heading_style, fontSize=max(16 - level, 10), spaceAfter=8, spaceBefore=16 if level <= 2 else 12)
                                story.append(Paragraph(header_text, header_style))
                        else:
                            processed_line = PDFConverter._process_inline_markdown(line)
                            story.append(Paragraph(processed_line, normal_style))
                            story.append(Spacer(1, 6))
                else:
                    logging.info(f'Processing plain text file with {len(text_content)} characters...')
                    lines = text_content.split('\n')
                    line_count = 0
                    for line in lines:
                        line = line.rstrip()
                        line_count += 1
                        if not line.strip():
                            story.append(Spacer(1, 6))
                            continue
                        safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(safe_line, normal_style))
                        story.append(Spacer(1, 3))
                    logging.info(f'Added {line_count} lines to PDF')
                    if not story:
                        story.append(Paragraph('(Empty text file)', normal_style))
                doc.build(story)
                logging.info(f'Successfully converted {text_path.name} to PDF ({pdf_path.stat().st_size / 1024:.1f} KB)')
            except ImportError:
                raise RuntimeError('reportlab is required for text-to-PDF conversion. Please install it using: pip install reportlab')
            except Exception as e:
                raise RuntimeError(f'Failed to convert text file {text_path.name} to PDF: {str(e)}')
            if not pdf_path.exists() or pdf_path.stat().st_size < 100:
                raise RuntimeError(f'PDF conversion failed for {text_path.name} - generated PDF is empty or corrupted.')
            return pdf_path
        except Exception as e:
            logging.error(f'Error in convert_text_to_pdf: {str(e)}')
            raise

    @staticmethod
    def _process_inline_markdown(text: str) -> str:
        """
        Process inline markdown formatting (bold, italic, code, links)

        Args:
            text: Raw text with markdown formatting

        Returns:
            Text with ReportLab markup
        """
        import re
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = re.sub('\\*\\*(.*?)\\*\\*', '<b>\\1</b>', text)
        text = re.sub('__(.*?)__', '<b>\\1</b>', text)
        text = re.sub('(?<!\\w)\\*([^*\\n]+?)\\*(?!\\w)', '<i>\\1</i>', text)
        text = re.sub('(?<!\\w)_([^_\\n]+?)_(?!\\w)', '<i>\\1</i>', text)
        text = re.sub('`([^`]+?)`', '<font name="Courier" size="9" color="darkred">\\1</font>', text)

        def link_replacer(match):
            link_text = match.group(1)
            url = match.group(2)
            return f'<link href="{url}" color="blue"><u>{link_text}</u></link>'
        text = re.sub('\\[([^\\]]+?)\\]\\(([^)]+?)\\)', link_replacer, text)
        text = re.sub('~~(.*?)~~', '<strike>\\1</strike>', text)
        return text

    def convert_to_pdf(self, file_path: Union[str, Path], output_dir: Optional[str]=None) -> Path:
        """
        Convert document to PDF based on file extension

        Args:
            file_path: Path to the file to be converted
            output_dir: Output directory path

        Returns:
            Path to the generated PDF file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f'File does not exist: {file_path}')
        ext = file_path.suffix.lower()
        if ext in self.OFFICE_FORMATS:
            return self.convert_office_to_pdf(file_path, output_dir)
        elif ext in self.TEXT_FORMATS:
            return self.convert_text_to_pdf(file_path, output_dir)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: {', '.join(self.OFFICE_FORMATS | self.TEXT_FORMATS)}")

    def check_dependencies(self) -> dict:
        """
        Check if required dependencies are available

        Returns:
            dict: Dictionary with dependency check results
        """
        results = {'libreoffice': False, 'reportlab': False}
        try:
            subprocess_kwargs: Dict[str, Any] = {'capture_output': True, 'text': True, 'check': True, 'encoding': 'utf-8', 'errors': 'ignore'}
            if platform.system() == 'Windows':
                subprocess_kwargs['creationflags'] = 134217728
            subprocess.run(['libreoffice', '--version'], **subprocess_kwargs)
            results['libreoffice'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(['soffice', '--version'], **subprocess_kwargs)
                results['libreoffice'] = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        import importlib.util
        if importlib.util.find_spec('reportlab') is not None:
            results['reportlab'] = True
        return results