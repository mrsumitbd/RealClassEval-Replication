from alerta.exceptions import ApiError

class QueryBuilder:

    @staticmethod
    def sort_by_columns(params, valid_params):
        sort = list()
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
                direction = 'ASC' if direction * reverse == 1 else 'DESC'
                if attribute:
                    sort.append(f"attributes->'{attribute}' {direction}")
                else:
                    sort.append(f'{column} {direction}')
        else:
            sort.append('(select 1)')
        return sort

    @staticmethod
    def filter_query(params, valid_params, query, qvars):
        for field in params.keys():
            if field.replace('!', '').split('.')[0] in EXCLUDE_FROM_QUERY:
                continue
            valid_filter_params = [k for k, v in valid_params.items() if v[0]]
            if field.replace('!', '').split('.')[0] not in valid_filter_params:
                raise ApiError(f'Invalid filter parameter: {field}', 400)
            column, _, _ = valid_params[field.replace('!', '').split('.')[0]]
            value = params.getlist(field)
            if field in ['service', 'tags', 'roles', 'scopes']:
                query.append('AND {0} && %({0})s'.format(column))
                qvars[column] = value
            elif field.startswith('attributes.'):
                column = field.replace('attributes.', '')
                query.append(f'AND attributes @> %(attr_{column})s')
                qvars['attr_' + column] = {column: value[0]}
            elif len(value) == 1:
                value = value[0]
                if field.endswith('!'):
                    if value.startswith('~'):
                        query.append('AND NOT "{0}" ILIKE %(not_{0})s'.format(column))
                        qvars['not_' + column] = '%' + value[1:] + '%'
                    else:
                        query.append('AND "{0}"!=%(not_{0})s'.format(column))
                        qvars['not_' + column] = value
                elif value.startswith('~'):
                    query.append('AND "{0}" ILIKE %({0})s'.format(column))
                    qvars[column] = '%' + value[1:] + '%'
                else:
                    query.append('AND "{0}"=%({0})s'.format(column))
                    qvars[column] = value
            elif field.endswith('!'):
                if '~' in [v[0] for v in value]:
                    query.append('AND "{0}" !~* (%(not_regex_{0})s)'.format(column))
                    qvars['not_regex_' + column] = '|'.join([v.lstrip('~') for v in value])
                else:
                    query.append('AND NOT "{0}"=ANY(%(not_{0})s)'.format(column))
                    qvars['not_' + column] = value
            elif '~' in [v[0] for v in value]:
                query.append('AND "{0}" ~* (%(regex_{0})s)'.format(column))
                qvars['regex_' + column] = '|'.join([v.lstrip('~') for v in value])
            else:
                query.append('AND "{0}"=ANY(%({0})s)'.format(column))
                qvars[column] = value
        return (query, qvars)