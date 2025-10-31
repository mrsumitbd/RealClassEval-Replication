class CodePageManager:
    '''Holds information about all the code pages.
    Information as defined in escpos-printer-db.
        '''

    _encodings = {}
    _alias_to_name = {}

    def __init__(self, data):
        '''Initialize code page manager.'''
        # Normalize data into a canonical mapping: name -> info
        enc_map = {}

        def add_alias(canon_name, alias):
            if not alias:
                return
            key = str(alias).strip().lower()
            if key:
                self.__class__._alias_to_name[key] = canon_name

        if isinstance(data, dict):
            # If dict looks like direct name->info mapping
            # or holds a list under a common key, handle both.
            candidates = None
            for k in ('encodings', 'codepages', 'code_pages'):
                if k in data and isinstance(data[k], list):
                    candidates = data[k]
                    break
            if candidates is not None:
                for item in candidates:
                    if not isinstance(item, dict):
                        continue
                    name = str(item.get('name') or item.get(
                        'encoding') or '').strip()
                    if not name:
                        continue
                    canon = name.lower()
                    enc_map[canon] = item
                    # aliases
                    aliases = item.get('aliases') or item.get('alias') or []
                    if isinstance(aliases, str):
                        aliases = [aliases]
                    for al in aliases:
                        add_alias(canon, al)
                    # numeric/id aliases
                    num = item.get(
                        'id') if 'id' in item else item.get('number')
                    if isinstance(num, int) or (isinstance(num, str) and num.isdigit()):
                        num_str = str(num)
                        add_alias(canon, num_str)
                        add_alias(canon, f'cp{num_str}')
                        add_alias(canon, f'ibm{num_str}')
                    # also map the original name itself as alias
                    add_alias(canon, name)
            else:
                # Treat keys as canonical names
                for name, info in data.items():
                    canon = str(name).strip().lower()
                    if not canon:
                        continue
                    enc_map[canon] = info if isinstance(
                        info, dict) else {'data': info}
                    aliases = []
                    if isinstance(info, dict):
                        aliases = info.get(
                            'aliases') or info.get('alias') or []
                    if isinstance(aliases, str):
                        aliases = [aliases]
                    for al in aliases:
                        add_alias(canon, al)
                    # numeric/id aliases
                    num = None
                    if isinstance(info, dict):
                        num = info.get(
                            'id') if 'id' in info else info.get('number')
                    if isinstance(num, int) or (isinstance(num, str) and str(num).isdigit()):
                        num_str = str(num)
                        add_alias(canon, num_str)
                        add_alias(canon, f'cp{num_str}')
                        add_alias(canon, f'ibm{num_str}')
                    add_alias(canon, name)
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                name = str(item.get('name') or item.get(
                    'encoding') or '').strip()
                if not name:
                    continue
                canon = name.lower()
                enc_map[canon] = item
                aliases = item.get('aliases') or item.get('alias') or []
                if isinstance(aliases, str):
                    aliases = [aliases]
                for al in aliases:
                    add_alias(canon, al)
                num = item.get('id') if 'id' in item else item.get('number')
                if isinstance(num, int) or (isinstance(num, str) and str(num).isdigit()):
                    num_str = str(num)
                    add_alias(canon, num_str)
                    add_alias(canon, f'cp{num_str}')
                    add_alias(canon, f'ibm{num_str}')
                add_alias(canon, name)

        # Merge into class-level registries
        # Later initializations can extend/override previous ones.
        self.__class__._encodings.update(enc_map)

    @staticmethod
    def get_encoding_name(encoding):
        '''Get encoding name.
        .. todo:: Resolve the encoding alias.
        '''
        if encoding is None:
            return None
        key = str(encoding).strip().lower()
        if not key:
            return None
        # Direct canonical name
        if key in CodePageManager._encodings:
            return key
        # Alias resolution
        return CodePageManager._alias_to_name.get(key)

    def get_encoding_name(encoding):
        '''Return the encoding data.'''
        # This method is defined without decorators and will typically be called
        # as CodePageManager.get_encoding_name(value)
        name = CodePageManager.get_encoding_name.__func__(encoding) if hasattr(
            CodePageManager.get_encoding_name, '__func__') else CodePageManager.get_encoding_name(encoding)  # resolve canonical name
        # After the line above, name is either canonical name or None.
        if not name:
            return None
        return CodePageManager._encodings.get(name)
