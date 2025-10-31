import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


class PDFHandler:
    """
    The class allows merging multiple PDF files into one and extracting text from PDFs using PyPDF2 library.
    """

    def __init__(self, filepaths):
        """
        takes a list of file paths filepaths as a parameter.
        It creates a list named readers using PyPDF2, where each reader opens a file from the given paths.
        """
        self.filepaths = list(filepaths) if filepaths is not None else []
        self._file_objs = []
        self.readers = []
        for fp in self.filepaths:
            fobj = open(fp, "rb")
            self._file_objs.append(fobj)
            # Support both old and new PyPDF2 APIs
            try:
                reader = PyPDF2.PdfFileReader(fobj)
            except AttributeError:
                # Newer versions use PdfReader
                reader = PyPDF2.PdfReader(fobj)
            self.readers.append(reader)

    def merge_pdfs(self, output_filepath):
        """
        Read files in self.readers which stores handles to multiple PDF files.
        Merge them to one pdf and update the page number, then save in disk.
        :param output_filepath: str, ouput file path to save to
        :return: str, "Merged PDFs saved at {output_filepath}" if successfully merged
        >>> handler = PDFHandler(['a.pdf', 'b.pdf'])
        >>> handler.merge_pdfs('out.pdf')
        Merged PDFs saved at out.pdf
        """
        if not self.readers:
            raise ValueError("No PDF readers available to merge.")

        # Prefer PdfFileMerger when available; fall back to writer if needed
        merger = None
        try:
            merger = PdfFileMerger()
        except Exception:
            merger = None

        if merger is not None:
            for rdr in self.readers:
                merger.append(rdr)
            with open(output_filepath, "wb") as out_f:
                merger.write(out_f)
            # close internal handles of merger if any
            try:
                merger.close()
            except Exception:
                pass
        else:
            # Fallback: manual copy using writer
            try:
                writer = PdfFileWriter()
            except Exception:
                writer = PyPDF2.PdfWriter()
            for rdr in self.readers:
                # Support both APIs
                try:
                    num_pages = rdr.getNumPages()
                    def get_page(i): return rdr.getPage(i)
                except AttributeError:
                    num_pages = len(rdr.pages)
                    def get_page(i): return rdr.pages[i]
                for i in range(num_pages):
                    page = get_page(i)
                    try:
                        writer.addPage(page)
                    except AttributeError:
                        writer.add_page(page)
            with open(output_filepath, "wb") as out_f:
                try:
                    writer.write(out_f)
                except TypeError:
                    writer.write(out_f)

        return f"Merged PDFs saved at {output_filepath}"

    def extract_text_from_pdfs(self):
        """
        Extract text from pdf files in self.readers
        :return pdf_texts: list of str, each element is the text of one pdf file
        >>> handler = PDFHandler(['a.pdf', 'b.pdf'])
        >>> handler.extract_text_from_pdfs()
        ['Test a.pdf', 'Test b.pdf']
        """
        texts = []
        for rdr in self.readers:
            # Determine page count and retrieval across versions
            try:
                num_pages = rdr.getNumPages()
                def get_page(i): return rdr.getPage(i)
            except AttributeError:
                num_pages = len(rdr.pages)
                def get_page(i): return rdr.pages[i]
            chunks = []
            for i in range(num_pages):
                page = get_page(i)
                # Support both extract_text and extractText
                txt = ""
                try:
                    txt = page.extract_text()
                except AttributeError:
                    try:
                        txt = page.extractText()
                    except Exception:
                        txt = ""
                if txt:
                    chunks.append(txt)
            texts.append("".join(chunks))
        return texts

    def __del__(self):
        # Ensure file handles are closed
        for f in getattr(self, "_file_objs", []):
            try:
                f.close()
            except Exception:
                pass
