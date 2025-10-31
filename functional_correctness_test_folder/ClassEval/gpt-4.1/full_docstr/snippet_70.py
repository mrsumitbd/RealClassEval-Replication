
import PyPDF2


class PDFHandler:
    """
    The class allows merging multiple PDF files into one and extracting text from PDFs using PyPDF2 library.
    """

    def __init__(self, filepaths):
        """
        takes a list of file paths filepaths as a parameter.
        It creates a list named readers using PyPDF2, where each reader opens a file from the given paths.
        """
        self.filepaths = filepaths
        self.readers = []
        self._file_objs = []
        for fp in filepaths:
            f = open(fp, "rb")
            self._file_objs.append(f)
            self.readers.append(PyPDF2.PdfFileReader(f))

    def merge_pdfs(self, output_filepath):
        """
        Read files in self.readers which stores handles to multiple PDF files.
        Merge them to one pdf and update the page number, then save in disk.
        :param output_filepath: str, ouput file path to save to
        :return: str, "Merged PDFs saved at {output_filepath}" if successfully merged
        """
        merger = PyPDF2.PdfFileMerger()
        for fp in self.filepaths:
            merger.append(fp)
        with open(output_filepath, "wb") as fout:
            merger.write(fout)
        merger.close()
        return f"Merged PDFs saved at {output_filepath}"

    def extract_text_from_pdfs(self):
        """
        Extract text from pdf files in self.readers
        :return pdf_texts: list of str, each element is the text of one pdf file
        """
        pdf_texts = []
        for reader in self.readers:
            text = ""
            for page_num in range(reader.getNumPages()):
                page = reader.getPage(page_num)
                if hasattr(page, "extract_text"):
                    # PyPDF2 >= 2.0.0
                    page_text = page.extract_text()
                else:
                    # PyPDF2 < 2.0.0
                    page_text = page.extractText()
                if page_text:
                    text += page_text
            pdf_texts.append(text)
        return pdf_texts

    def __del__(self):
        for f in getattr(self, "_file_objs", []):
            try:
                f.close()
            except Exception:
                pass
