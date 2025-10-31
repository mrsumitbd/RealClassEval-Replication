from os.path import isfile, join
import os
from acw_db import ACW_DB
import sys
import pathlib
from datetime import datetime
from zipfile import ZipFile

class AutoZipper:

    def __init__(self):
        config_base_dir = os.environ.get('ACW_CONFIG_DIR', '/config')
        self.archive_dirs_stem = os.path.join(config_base_dir, 'processed_books')
        self.converted_dir = os.path.join(self.archive_dirs_stem, 'converted')
        self.failed_dir = os.path.join(self.archive_dirs_stem, 'failed')
        self.imported_dir = os.path.join(self.archive_dirs_stem, 'imported')
        self.fixed_originals_dir = os.path.join(self.archive_dirs_stem, 'fixed_originals')
        self.archive_dirs = [self.converted_dir, self.failed_dir, self.imported_dir, self.fixed_originals_dir]
        self.current_date = datetime.today().strftime('%Y-%m-%d')
        self.db = ACW_DB()
        self.acw_settings = self.db.acw_settings
        if not self.acw_settings.get('auto_zip_backups', False):
            print('[acw-auto-zipper] Cancelling Auto-Zipper as the service is currently disabled in the acw-settings panel. Exiting...')
            sys.exit(0)
        self.to_zip = self.get_books_to_zip()

    def last_mod_date(self, path_to_file) -> str:
        """ Returns the date a given file was last modified as a string """
        stat = os.stat(path_to_file)
        return datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

    def get_books_to_zip(self) -> dict[str, list[str]]:
        """ Returns a dictionary with the books that are to be zipped together in each dir """
        to_zip = {}
        for dir_path in self.archive_dirs:
            if not os.path.isdir(dir_path):
                print(f'[acw-auto-zipper] Warning: Directory not found: {dir_path}. Skipping.')
                continue
            dir_name = os.path.basename(dir_path)
            books = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f)) and pathlib.Path(f).suffix != '.zip']
            to_zip_in_dir = []
            for book in books:
                full_book_path = os.path.join(dir_path, book)
                if self.last_mod_date(full_book_path) == self.current_date:
                    to_zip_in_dir.append(full_book_path)
            to_zip |= {dir_name: to_zip_in_dir}
        return to_zip

    def zip_todays_books(self) -> bool:
        """ Zips the files in self.to_zip for each respective dir together if new files are found in each. If no files are zipped, the bool returned is false. """
        zip_indicator = False
        for dir_path in self.archive_dirs:
            dir_name = os.path.basename(dir_path)
            if len(self.to_zip[dir_name]) > 0:
                zip_indicator = True
                zip_filename = f'{self.current_date}-{dir_name}.zip'
                zip_filepath = os.path.join(self.archive_dirs_stem, dir_name, zip_filename)
                os.makedirs(os.path.dirname(zip_filepath), exist_ok=True)
                with ZipFile(zip_filepath, 'w') as zip_file_obj:
                    for file_to_zip in self.to_zip[dir_name]:
                        zip_file_obj.write(file_to_zip, arcname=os.path.basename(file_to_zip))
        return zip_indicator

    def remove_zipped_files(self) -> None:
        """ Deletes files following their successful compression """
        for dir_path in self.archive_dirs:
            dir_name = os.path.basename(dir_path)
            for file_to_remove in self.to_zip[dir_name]:
                if os.path.exists(file_to_remove):
                    os.remove(file_to_remove)
                else:
                    print(f'[acw-auto-zipper] Warning: File not found for removal: {file_to_remove}')