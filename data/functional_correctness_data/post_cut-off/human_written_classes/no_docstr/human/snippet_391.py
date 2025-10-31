import os
from urllib.parse import urlparse
import json

class Document:

    def __init__(self):
        self.content = []
        self.keyframes = []

    def document_analysis(self, document_path):
        import xmltodict
        error = None
        self.content = []
        self.keyframes = []
        try:
            if not os.path.exists(document_path):
                raise FileNotFoundError(f'File not found at path: {document_path}')
            file_extension = os.path.splitext(document_path)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png']:
                parsed_url = urlparse(document_path)
                is_url = all([parsed_url.scheme, parsed_url.netloc])
                if not is_url:
                    base64_image = encode_image_from_file(document_path)
                else:
                    base64_image = encode_image_from_url(document_path)
                self.content = f'data:image/jpeg;base64,{base64_image}'
                return (self.content, self.keyframes, error)
            elif file_extension in ['.xls', '.xlsx']:
                try:
                    import pandas as pd
                except ImportError:
                    error = 'pandas library not found. Please install pandas: pip install pandas'
                    return (self.content, self.keyframes, error)
                excel_data = {}
                try:
                    with pd.ExcelFile(document_path) as xls:
                        for sheet_name in xls.sheet_names:
                            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                            df.fillna('', inplace=True)
                            excel_data[sheet_name] = df.values.tolist()
                    self.content = json.dumps(excel_data, ensure_ascii=False)
                    logger.info(f'Successfully processed Excel file: {document_path}')
                except Exception as excel_error:
                    error = str(excel_error)
                return (self.content, self.keyframes, error)
            elif file_extension in ['.json', '.jsonl', '.jsonld']:
                with open(document_path, 'r', encoding='utf-8') as f:
                    self.content = json.load(f)
                return (self.content, self.keyframes, error)
            elif file_extension == '.xml':
                with open(document_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                try:
                    self.content = xmltodict.parse(data)
                except Exception as e:
                    error = str(e)
                    self.content = data
                return (self.content, self.keyframes, error)
            elif file_extension in ['.doc', '.docx']:
                from docx2markdown import docx_to_markdown
                md_file_path = f'{os.path.basename(document_path)}.md'
                docx_to_markdown(document_path, md_file_path)
                with open(md_file_path, 'r') as f:
                    self.content = f.read()
                os.remove(md_file_path)
                return (self.content, self.keyframes, error)
            elif file_extension == '.pdf':
                try:
                    from PyPDF2 import PdfReader
                    with open(document_path, 'rb') as f:
                        reader = PdfReader(f)
                        self.content = ''.join((page.extract_text() for page in reader.pages if page.extract_text()))
                except Exception as pdf_error:
                    error = str(pdf_error)
                    return (self.content, self.keyframes, error)
            elif any((document_path.endswith(ext.lower()) for ext in ['.mp3', '.wav', '.wave', '.m4a'])):
                return (self.content, self.keyframes, error)
            elif any((document_path.endswith(ext.lower()) for ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'])):
                return (self.content, self.keyframes, error)
            elif any((document_path.endswith(ext) for ext in ['pptx'])):
                return (self.content, self.keyframes, error)
        except FileNotFoundError as fnf_error:
            error = str(fnf_error)
        except Exception as e:
            error = f'An unexpected error occurred in document_analysis: {e}'
        return (self.content, self.keyframes, error)

    def read_document(self, file_path):
        error = None
        content = None
        try:
            content, keyframes, error = self.document_analysis(file_path)
        except Exception as e:
            error = str(e)
        result = {'content': content}
        if keyframes:
            result['keyframes'] = keyframes
        if error:
            result['error'] = error
        return json.dumps(result, ensure_ascii=False)