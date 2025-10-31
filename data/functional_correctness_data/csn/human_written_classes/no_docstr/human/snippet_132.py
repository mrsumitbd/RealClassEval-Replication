import re
from alerta.exceptions import ApiError

class QueryBuilder:

    @staticmethod
    def sort_by_columns(params, valid_params):
        sort = list()
        direction = 1
        if params.get('sort-by', None):
            for sort_by in params.getlist('sort-by'):
                reverse = 1
                attribute = None
                if sort_by.startswith('-'):
                    reverse = -1
                    sort_by = sort_by[1:]
                if sort_by.startswith('attributes.'):
                    attribute = sort_by.split('.')[1]
                    sort_by = 'attributes'
                valid_sort_params = [k for k, v in valid_params.items() if v[1]]
                if sort_by not in valid_sort_params:
                    raise ApiError(f"Sorting by '{sort_by}' field not supported.", 400)
                _, column, direction = valid_params[sort_by]
                if attribute:
                    column = f'attributes.{attribute}'
                sort.append((column, direction * reverse))
        else:
            sort.append(('_id', direction))
        return sort

    @staticmethod
    def filter_query(params, valid_params, query):
        for field in params.keys():
            if field.replace('!', '').split('.')[0] in EXCLUDE_FROM_QUERY:
                continue
            if field.replace('!', '').split('.')[0] not in valid_params:
                raise ApiError(f'Invalid filter parameter: {field}', 400)
            if field.startswith('attributes.'):
                column = field
            else:
                column, _, _ = valid_params[field.replace('!', '').split('.')[0]]
            value = params.getlist(field)
            if len(value) == 1:
                value = value[0]
                if field.endswith('!'):
                    if value.startswith('~'):
                        query[column] = dict()
                        query[column]['$not'] = re.compile(value[1:], re.IGNORECASE)
                    else:
                        query[column] = dict()
                        query[column]['$ne'] = value
                elif value.startswith('~'):
                    query[column] = dict()
                    query[column]['$regex'] = re.compile(value[1:], re.IGNORECASE)
                else:
                    query[column] = value
            elif field.endswith('!'):
                if '~' in [v[0] for v in value]:
                    value = '|'.join([v.lstrip('~') for v in value])
                    query[column] = dict()
                    query[column]['$not'] = re.compile(value, re.IGNORECASE)
                else:
                    query[column] = dict()
                    query[column]['$nin'] = value
            elif '~' in [v[0] for v in value]:
                value = '|'.join([v.lstrip('~') for v in value])
                query[column] = dict()
                query[column]['$regex'] = re.compile(value, re.IGNORECASE)
            else:
                query[column] = dict()
                query[column]['$in'] = value
        return query