import json
from pypuppetdb.errors import APIError

class FunctionOperator:
    """
    Performs an aggregate function on the result of a subquery, full
    documentation is available at
    https://puppet.com/docs/puppetdb/7/api/query/v4/ast.html#function.
    This object can only be used in the field list or group by list of
    an ExtractOperator object.

    :param function: The name of the function to perform.
    :type function: :obj:`str`
    :param field: The name of the field to perform the function on. All
        functions with the exception of count require this value.
    :type field: :obj:`str`
    """

    def __init__(self, function, field=None, fmt=None):
        if function not in ['count', 'avg', 'sum', 'min', 'max', 'to_string']:
            raise APIError(f'Unsupport function: {function}')
        elif function != 'count' and field is None:
            raise APIError('Function {} requires a field value'.format(function))
        elif function == 'to_string' and fmt is None:
            raise APIError("Function {0} requires an extra 'fmt' parameter")
        self.arr = ['function', function]
        if field is not None:
            self.arr.append(field)
        if function == 'to_string':
            self.arr.append(fmt)

    def __repr__(self):
        return f'Query: {self}'

    def __str__(self):
        return json.dumps(self.json_data())

    def json_data(self):
        return self.arr