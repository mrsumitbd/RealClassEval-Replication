from addok.config import config

class FieldsIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        importance = float(doc.get('importance', 0.0)) * config.IMPORTANCE_WEIGHT
        for field in config.FIELDS:
            name = field['key']
            values = doc.get(name)
            if not values:
                if not field.get('null', True):
                    raise ValueError('{} must not be null'.format(name))
                continue
            if name != config.HOUSENUMBERS_FIELD:
                boost = field.get('boost', config.DEFAULT_BOOST)
                if callable(boost):
                    boost = boost(doc)
                boost = boost + importance
                values = check_type_and_transform_to_array(name, values)
                for value in values:
                    extract_tokens(tokens, str(value), boost=boost)
        index_tokens(pipe, tokens, key, **kwargs)

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        for field in config.FIELDS:
            name = field['key']
            if name == config.HOUSENUMBERS_FIELD:
                continue
            values = doc.get(name)
            if values:
                values = check_type_and_transform_to_array(name, values)
                for value in values:
                    tokens.extend(deindex_field(key, value))