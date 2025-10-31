from urllib.parse import parse_qs, quote, urlparse
import hashlib

class QshGenerator:

    def __init__(self, context_path):
        self.context_path = context_path

    def __call__(self, req):
        qsh = self._generate_qsh(req)
        return hashlib.sha256(qsh.encode('utf-8')).hexdigest()

    def _generate_qsh(self, req):
        parse_result = urlparse(req.url)
        path = parse_result.path[len(self.context_path):] if len(self.context_path) > 1 else parse_result.path
        params = parse_qs(parse_result.query, keep_blank_values=True)
        joined = {key: ','.join(self._sort_and_quote_values(params[key])) for key in params}
        query = '&'.join((f'{key}={joined[key]}' for key in sorted(joined.keys())))
        qsh = f'{req.method.upper()}&{path}&{query}'
        return qsh

    def _sort_and_quote_values(self, values):
        ordered_values = sorted(values)
        return [quote(value, safe='~') for value in ordered_values]