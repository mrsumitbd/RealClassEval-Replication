import json
from typing import Iterator, List, Any, Union, Optional, Dict

class KustoResultColumn:

    def __init__(self, json_column: Dict[str, Any], ordinal: int):
        self.column_name = json_column['ColumnName']
        self.column_type = json_column.get('ColumnType') or json_column['DataType']
        self.ordinal = ordinal

    def __repr__(self) -> str:
        return 'KustoResultColumn({},{})'.format(json.dumps({'ColumnName': self.column_name, 'ColumnType': self.column_type}), self.ordinal)