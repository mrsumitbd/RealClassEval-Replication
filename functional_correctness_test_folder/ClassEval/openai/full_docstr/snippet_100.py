
import os
import zipfile
from pathlib import Path


class ZipFileProcessor:
    """
    This is a compressed file processing class that provides the ability to read and decompress compressed files
    """

    def __init__(self, file_name):
        """
        Initialize file name
        :param file_name:string
        """
        self.file_name = file_name

    def read_zip_file(self):
        """
        Get open file object
        :return:If successful, returns the open file object; otherwise, returns None
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> file = zfp.read_zip_file()
        """
        try:
            return zipfile.ZipFile(self.file_name, 'r')
        except (FileNotFoundError, zipfile.BadZipFile):
            return None

    def extract_all(self, output_path):
        """
        Extract all zip files and place them in the specified path
        :param output_path: string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_all("result/aaa")
        """
        try:
            with self.read_zip_file() as zf:
                if zf is None:
                    return False
                Path(output_path).mkdir(parents=True, exist_ok=True)
                zf.extractall(path=output_path)
            return True
        except Exception:
            return False

    def extract_file(self, file_name, output_path):
        """
        Extract the file with the specified name from the zip file and place it in the specified path
        :param file_name:string, The name of the file to be uncompressed
        :param output_path:string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_file("bbb.txt", "result/aaa")
        """
        try:
            with self.read_zip_file() as zf:
                if zf is None:
                    return False
                if file_name not in zf.namelist():
                    return False
                Path(output_path).mkdir(parents=True, exist_ok=True)
                zf.extract(member=file_name, path=output_path)
            return True
        except Exception:
            return False

    def create_zip_file(self, files, output_file_name):
        """
        Compress the specified file list into a zip file and place it in the specified path
        :param files:list of string, List of files to compress
        :param output_file_name: string, Specified output path
        :return:True or False, representing whether the compression operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.create_zip_file(["bbb.txt", "ccc,txt", "ddd.txt"], "output/bcd")
        """
        try:
            output_path = Path(output_file_name)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(output_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for file in files:
                    if not os.path.isfile(file):
                        continue
                    zf.write(file, arcname=os.path.basename(file))
            return True
        except Exception:
            return False
