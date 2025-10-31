import json
import pathlib

class DataPackage:

    def __init__(self, spec, directory=None):
        if isinstance(spec, DataPackage):
            self.json = spec.json
            self.dir = spec.dir
            return
        if isinstance(spec, dict):
            self.dir = pathlib.Path(directory or '.')
        elif isinstance(spec, pathlib.Path):
            self.dir = directory or spec.parent
            spec = json.loads(spec.read_text(encoding='utf8'))
        else:
            spec = json.loads(spec)
            self.dir = pathlib.Path(directory or '.')
        self.json = spec

    def to_tablegroup(self, cls=None):
        from csvw import TableGroup
        md = {'@context': 'http://www.w3.org/ns/csvw'}
        md['dc:replaces'] = json.dumps(self.json)
        for flprop, csvwprop in [('id', 'dc:identifier'), ('licenses', 'dc:license'), ('title', 'dc:title'), ('homepage', 'dcat:accessURL'), ('description', 'dc:description'), ('sources', 'dc:source'), ('contributors', 'dc:contributor'), ('profile', 'dc:conformsTo'), ('keywords', 'dc:subject'), ('created', 'dc:created')]:
            if flprop in self.json:
                md[csvwprop] = self.json[flprop]
        if 'name' in self.json:
            if 'id' not in self.json:
                md['dc:identifier'] = self.json['name']
            elif 'title' not in self.json:
                md['dc:title'] = self.json['name']
        resources = [rsc for rsc in self.json.get('resources', []) if 'path' in rsc]
        resource_map = {rsc['name']: rsc['path'] for rsc in resources if 'name' in rsc}
        for rsc in resources:
            schema = rsc.get('schema')
            if schema and rsc.get('scheme') == 'file' and (rsc.get('format') == 'csv'):
                md.setdefault('tables', [])
                table = dict(url=rsc['path'], tableSchema=convert_table_schema(rsc.get('name'), schema, resource_map), dialect=convert_dialect(rsc))
                md['tables'].append(table)
        cls = cls or TableGroup
        res = cls.fromvalue(md)
        res._fname = self.dir / 'csvw-metadata.json'
        return res