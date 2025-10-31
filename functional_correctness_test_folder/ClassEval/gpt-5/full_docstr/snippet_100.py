import os
import zipfile
from pathlib import Path
from typing import List, Optional


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

    def read_zip_file(self) -> Optional[zipfile.ZipFile]:
        """
        Get open file object
        :return:If successful, returns the open file object; otherwise, returns None
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> file = zfp.read_zip_file()
        """
        try:
            if not self.file_name or not os.path.isfile(self.file_name):
                return None
            if not zipfile.is_zipfile(self.file_name):
                return None
            return zipfile.ZipFile(self.file_name, mode="r")
        except Exception:
            return None

    def extract_all(self, output_path) -> bool:
        """
        Extract all zip files and place them in the specified path
        :param output_path: string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_all("result/aaa")
        """
        zf = self.read_zip_file()
        if zf is None:
            return False
        try:
            Path(output_path).mkdir(parents=True, exist_ok=True)
            zf.extractall(path=output_path)
            return True
        except Exception:
            return False
        finally:
            try:
                zf.close()
            except Exception:
                pass

    def extract_file(self, file_name, output_path) -> bool:
        """
        Extract the file with the specified name from the zip file and place it in the specified path
        :param file_name:string, The name of the file to be uncompressed
        :param output_path:string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_file("bbb.txt", "result/aaa")
        """
        if not file_name:
            return False
        zf = self.read_zip_file()
        if zf is None:
            return False
        try:
            Path(output_path).mkdir(parents=True, exist_ok=True)
            # Normalize path separators inside zip
            members = zf.namelist()
            target = None
            for m in members:
                if m.rstrip("/").endswith(file_name):
                    target = m
                    break
            if target is None:
                return False
            zf.extract(member=target, path=output_path)
            return True
        except Exception:
            return False
        finally:
            try:
                zf.close()
            except Exception:
                pass

    def create_zip_file(self, files: List[str], output_file_name: str) -> bool:
        """
        Compress the specified file list into a zip file and place it in the specified path
        :param files:list of string, List of files to compress
        :param output_file_name: string, Specified output path
        :return:True or False, representing whether the compression operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.create_zip_file(["bbb.txt", "ccc,txt", "ddd.txt"], "output/bcd")
        """
        try:
            if not output_file_name:
                return False
            output_path = Path(output_file_name)
            if output_path.suffix.lower() != ".zip":
                output_path = output_path.with_suffix(".zip")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            def add_path(zf: zipfile.ZipFile, p: Path):
                if p.is_dir():
                    base = p.name
                    for root, _, filenames in os.walk(p):
                        root_path = Path(root)
                        for fn in filenames:
                            fpath = root_path / fn
                            rel = fpath.relative_to(p.parent)
                            zf.write(fpath, arcname=str(rel))
                elif p.is_file():
                    zf.write(p, arcname=p.name)

            with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                any_added = False
                for f in files or []:
                    p = Path(f)
                    if p.exists():
                        add_path(zf, p)
                        any_added = True
                if not any_added:
                    return False
            return True
        except Exception:
            return False
