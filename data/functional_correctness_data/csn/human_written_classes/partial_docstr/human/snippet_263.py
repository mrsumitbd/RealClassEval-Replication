import os
import sqlite3

class Dedup:
    """
    Stolen from warcprox
    https://github.com/internetarchive/warcprox/blob/master/warcprox/dedup.py
    """

    def __init__(self):
        self.file = os.path.join(args.archive_dir, 'dedup.db')

    def start(self):
        conn = sqlite3.connect(self.file)
        conn.execute('create table if not exists dedup (  key varchar(300) primary key,  value varchar(4000));')
        conn.commit()
        conn.close()

    def save(self, digest_key, url):
        conn = sqlite3.connect(self.file)
        conn.execute('insert or replace into dedup (key, value) values (?, ?)', (digest_key, url))
        conn.commit()
        conn.close()

    def lookup(self, digest_key, url=None):
        result = False
        conn = sqlite3.connect(self.file)
        cursor = conn.execute('select value from dedup where key = ?', (digest_key,))
        result_tuple = cursor.fetchone()
        conn.close()
        if result_tuple:
            result = True
        return result