import datetime
import json

class BinaryOperator:
    """
    This is a parent helper class used to create PuppetDB AST queries
    for single key-value pairs for the available operators.

    It is possible to directly declare the various types of queries
    from this class. For instance the code
    BinaryOperator('=', 'certname', 'node1.example.com') generates the
    PuppetDB query '["=", "certname", "node1.example.com"]'. It is preferred
    to use the child classes as they may have restrictions specific
    to that operator.

    See
    https://puppet.com/docs/puppetdb/7/api/query/v4/ast.html#binary-operators
    for more information.

    :param operator: The binary query operation performed. There is
        no value checking on this field.
    :type operator: :obj:`string`
    :param field: The PuppetDB endpoint query field. See endpoint
                  documentation for valid values.
    :type field: any
    :param value: The values of the field to match, or not match.
    :type value: any
    """

    def __init__(self, operator, field, value):
        if isinstance(value, datetime.datetime):
            value = str(value)
        self.data = [operator, field, value]

    def __repr__(self):
        return f'Query: {self}'

    def __str__(self):
        return json.dumps(self.json_data())

    def json_data(self):
        return self.data