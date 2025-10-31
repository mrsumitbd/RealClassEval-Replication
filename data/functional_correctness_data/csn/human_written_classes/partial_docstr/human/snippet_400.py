import sqlparse
import re

class Generalizator:
    """
    Class used to produce generalized sql out of given query
    """

    def __init__(self, sql: str=''):
        self._raw_query = sql

    @staticmethod
    def _normalize_likes(sql: str) -> str:
        """
        Normalize and wrap LIKE statements

        :type sql str
        :rtype: str
        """
        sql = sql.replace('%', '')
        sql = re.sub("LIKE '[^\\']+'", 'LIKE X', sql)
        matches = re.finditer('(or|and) [^\\s]+ LIKE X', sql, flags=re.IGNORECASE)
        matches = [match.group(0) for match in matches] if matches else None
        if matches:
            for match in set(matches):
                sql = re.sub('(\\s?' + re.escape(match) + ')+', ' ' + match + ' ...', sql)
        return sql

    @property
    def without_comments(self) -> str:
        """
        Removes comments from SQL query

        :rtype: str
        """
        sql = sqlparse.format(self._raw_query, strip_comments=True)
        sql = sql.replace('\n', ' ')
        sql = re.sub('[ \\t]+', ' ', sql)
        return sql

    @property
    def generalize(self) -> str:
        """
        Removes most variables from an SQL query
        and replaces them with X or N for numbers.

        Based on Mediawiki's DatabaseBase::generalizeSQL
        """
        if self._raw_query == '':
            return ''
        sql = self.without_comments
        sql = sql.replace('"', '')
        sql = re.sub('\\s{2,}', ' ', sql)
        sql = self._normalize_likes(sql)
        sql = re.sub('\\\\\\\\', '', sql)
        sql = re.sub("\\\\'", '', sql)
        sql = re.sub('\\\\"', '', sql)
        sql = re.sub("'[^\\']*'", 'X', sql)
        sql = re.sub('"[^\\"]*"', 'X', sql)
        sql = re.sub('\\s+', ' ', sql)
        sql = re.sub('-?[0-9]+', 'N', sql)
        sql = re.sub(' (IN|VALUES)\\s*\\([^,]+,[^)]+\\)', ' \\1 (XYZ)', sql, flags=re.IGNORECASE)
        return sql.strip()