import os
import subprocess
from datetime import datetime
import json
import sqlite3
from pathlib import Path
import re

class Book:

    def __init__(self, book_dir: str, file_path: str):
        self.book_dir: str = book_dir
        self.file_path: str = file_path
        self.calibre_library = self.get_calibre_library()
        self.file_format: str = Path(file_path).suffix.replace('.', '')
        self.timestamp: str = self.get_time()
        self.book_id: str = list(re.findall('\\(\\d*\\)', book_dir))[-1][1:-1]
        self.book_title, self.author_name, self.title_author = self.get_title_and_author()
        self.calibre_env = os.environ.copy()
        self.calibre_env['HOME'] = os.environ.get('ACW_CONFIG_DIR', '/config')
        self.split_library = self.get_split_library()
        if self.split_library:
            self.calibre_library = self.split_library['split_path']
            self.calibre_env['CALIBRE_OVERRIDE_DATABASE_PATH'] = os.path.join(self.split_library['db_path'], 'metadata.db')
        self.cover_path = book_dir + '/cover.jpg'
        self.old_metadata_path = book_dir + '/metadata.opf'
        self.new_metadata_path = self.get_new_metadata_path()
        self.log_info = None

    def get_split_library(self) -> dict[str, str] | None:
        config_dir = os.environ.get('ACW_CONFIG_DIR', '/config')
        app_db_file = os.path.join(config_dir, 'app.db')
        con = sqlite3.connect(app_db_file)
        cur = con.cursor()
        split_library = cur.execute('SELECT config_calibre_split FROM settings;').fetchone()[0]
        if split_library:
            split_path = cur.execute('SELECT config_calibre_split_dir FROM settings;').fetchone()[0]
            db_path = cur.execute('SELECT config_calibre_dir FROM settings;').fetchone()[0]
            con.close()
            return {'split_path': split_path, 'db_path': db_path}
        else:
            con.close()
            return None

    def get_calibre_library(self) -> str:
        """Gets Calibre-Library location from dirs_json path"""
        with open(dirs_json, 'r') as f:
            dirs = json.load(f)
        return dirs['calibre_library_dir']

    def get_time(self) -> str:
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def get_title_and_author(self) -> tuple[str, str, str]:
        title_author = self.file_path.split('/')[-1].split(f'.{self.file_format}')[0]
        book_title = title_author.split(f" - {title_author.split(' - ')[-1]}")[0]
        author_name = title_author.split(' - ')[-1]
        return (book_title, author_name, title_author)

    def get_new_metadata_path(self) -> str:
        """Uses the export function of the calibredb utility to export any new metadata for the given book to metadata_temp, and returns the path to the new metadata.opf"""
        subprocess.run(['calibredb', 'export', '--with-library', self.calibre_library, '--to-dir', metadata_temp_dir, self.book_id], env=self.calibre_env, check=True)
        temp_files = [os.path.join(dirpath, f) for dirpath, dirnames, filenames in os.walk(metadata_temp_dir) for f in filenames]
        return [f for f in temp_files if f.endswith('.opf')][0]

    def export_as_dict(self) -> dict[str, str | None]:
        return {'book_dir': self.book_dir, 'file_path': self.file_path, 'calibre_library': self.calibre_library, 'file_format': self.file_format, 'timestamp': self.timestamp, 'book_id': self.book_id, 'book_title': self.book_title, 'author_name': self.author_name, 'title_author': self.title_author, 'cover_path': self.cover_path, 'old_metadata_path': self.old_metadata_path, 'self.new_metadata_path': self.new_metadata_path, 'log_info': self.log_info}