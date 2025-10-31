from typing import Any, Dict, List, Optional, Tuple


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        if not isinstance(server_name, str) or not server_name.strip():
            return False
        servers, _errors = self.get_servers_data(app_context=app_context)
        target = server_name.strip().lower()
        for srv in servers:
            name = srv.get('name')
            if isinstance(name, str) and name.strip().lower() == target:
                return True
        return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        errors: List[str] = []
        servers_normalized: List[Dict[str, Any]] = []

        # Resolve context
        ctx = app_context
        if ctx is None:
            ctx = getattr(self, 'app_context', None)

        if ctx is None:
            errors.append('No application context provided.')
            return servers_normalized, errors

        raw = None

        # Try common patterns to get servers data
        try_sources = [
            lambda c: c.get_servers_data() if hasattr(c, 'get_servers_data') and callable(
                getattr(c, 'get_servers_data')) else None,
            lambda c: getattr(c, 'servers_data', None),
            lambda c: c.get_servers() if hasattr(c, 'get_servers') and callable(
                getattr(c, 'get_servers')) else None,
            lambda c: getattr(c, 'servers', None),
            lambda c: getattr(getattr(c, 'discovery', None), 'servers', None),
            lambda c: getattr(getattr(c, 'config', None), 'servers', None),
            lambda c: getattr(getattr(c, 'settings', None), 'servers', None),
        ]

        for getter in try_sources:
            try:
                raw = getter(ctx)
            except Exception as exc:
                errors.append(f'Error accessing servers data: {exc!r}')
                raw = None
            if raw:
                break

        if raw is None:
            errors.append('No servers data found in context.')
            return servers_normalized, errors

        # Normalize various shapes into List[Dict[str, Any]] with at least a "name" key
        def add_entry(name: Optional[str], data: Optional[Dict[str, Any]] = None) -> None:
            if not isinstance(name, str) or not name.strip():
                errors.append(
                    'Encountered server entry with invalid or missing name.')
                return
            entry = dict(data or {})
            entry.setdefault('name', name.strip())
            servers_normalized.append(entry)

        try:
            if isinstance(raw, dict):
                # Could be {name: data} or already normalized with keys like "items"
                # Prefer treating as mapping name->data if keys look like names
                all_values_are_dicts = all(isinstance(v, dict)
                                           for v in raw.values())
                if all_values_are_dicts:
                    for k, v in raw.items():
                        add_entry(str(k), v)
                else:
                    # Fallback: if dict has "items" or similar
                    items = None
                    for key in ('items', 'servers', 'data'):
                        if key in raw and isinstance(raw[key], list):
                            items = raw[key]
                            break
                    if items is None:
                        errors.append('Unrecognized servers dict structure.')
                    else:
                        raw = items  # proceed to list handling

            if isinstance(raw, list):
                for item in raw:
                    if isinstance(item, dict):
                        name = item.get('name') or item.get('id') or item.get(
                            'server') or item.get('hostname')
                        if not name and len(item) == 1:
                            # single-key dict like {"srv1": {...}}
                            k = next(iter(item))
                            v = item[k]
                            if isinstance(v, dict):
                                add_entry(str(k), v)
                            else:
                                add_entry(str(k), {'value': v})
                        else:
                            add_entry(
                                str(name) if name is not None else None, item)
                    elif isinstance(item, str):
                        add_entry(item, {})
                    else:
                        errors.append(
                            f'Unsupported server item type: {type(item).__name__}')
            elif isinstance(raw, (set, tuple)):
                for item in raw:
                    if isinstance(item, str):
                        add_entry(item, {})
                    else:
                        errors.append(
                            f'Unsupported server item type: {type(item).__name__}')
            elif isinstance(raw, dict) and not servers_normalized:
                # already handled above; if nothing added, mark error
                if not servers_normalized:
                    errors.append(
                        'Failed to normalize servers data from mapping.')
        except Exception as exc:
            errors.append(f'Failed to normalize servers data: {exc!r}')

        # Deduplicate by name (case-insensitive)
        seen = set()
        deduped: List[Dict[str, Any]] = []
        for s in servers_normalized:
            name = s.get('name')
            key = name.strip().lower() if isinstance(name, str) else None
            if not key:
                continue
            if key in seen:
                continue
            seen.add(key)
            deduped.append(s)

        return deduped, errors
