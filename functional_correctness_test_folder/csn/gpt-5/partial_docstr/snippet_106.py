class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def _get_root(tree):
        try:
            # xml.etree.ElementTree.ElementTree
            return tree.getroot()
        except AttributeError:
            # Already an Element
            return tree

    @staticmethod
    def _find(root, location):
        # Accept ElementPath string or a list/tuple of tags
        if isinstance(location, (list, tuple)):
            elem = root
            for tag in location:
                if elem is None:
                    return None
                elem = elem.find(tag)
            return elem
        else:
            return root.find(location)

    @staticmethod
    def _cast_value(text, force_string=False):
        if force_string:
            return '' if text is None else str(text)

        if text is None:
            return None

        s = str(text).strip()
        if s == '':
            return ''

        sl = s.lower()
        if sl in ('true', 'false'):
            return sl == 'true'

        # Try int
        try:
            if s.isdigit() or (s.startswith(('+', '-')) and s[1:].isdigit()):
                return int(s)
        except Exception:
            pass

        # Try float
        try:
            return float(s)
        except Exception:
            pass

        return s

    @staticmethod
    def getdata(tree, location, force_string=False):
        root = XMLStorage._get_root(tree)

        # Support attribute selection if location ends with '@attr' or contains '/@attr'
        attr_name = None
        elem = None

        if isinstance(location, str) and '@' in location:
            # Split at last '/@' or at '@' if no slash
            if '/@' in location:
                path, attr_name = location.rsplit('/@', 1)
            else:
                path, attr_name = location.split('@', 1)
            elem = XMLStorage._find(root, path)
            if elem is None:
                return None
            val = elem.get(attr_name)
            return XMLStorage._cast_value(val, force_string=force_string)
        else:
            elem = XMLStorage._find(root, location)

        if elem is None:
            return None

        # If element has no text but has exactly one attribute, return that attribute
        text = elem.text
        if (text is None or str(text).strip() == '') and len(elem.attrib) == 1 and not force_string:
            only_attr_val = next(iter(elem.attrib.values()))
            return XMLStorage._cast_value(only_attr_val, force_string=force_string)

        return XMLStorage._cast_value(text, force_string=force_string)

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        root = XMLStorage._get_root(tree)
        elem = XMLStorage._find(root, location)
        if elem is None:
            return None

        def _to_float(v):
            try:
                return float(str(v).strip())
            except Exception:
                return None

        # Case 1: attributes x, y, z on the element
        if all(k in elem.attrib for k in ('x', 'y', 'z')):
            x = _to_float(elem.attrib.get('x'))
            y = _to_float(elem.attrib.get('y'))
            z = _to_float(elem.attrib.get('z'))
            if None not in (x, y, z):
                return (x, y, z)

        # Case 2: child elements <x>, <y>, <z>
        cx = elem.find('x')
        cy = elem.find('y')
        cz = elem.find('z')
        if all(c is not None for c in (cx, cy, cz)):
            x = _to_float(cx.text)
            y = _to_float(cy.text)
            z = _to_float(cz.text)
            if None not in (x, y, z):
                return (x, y, z)

        # Case 3: text content with three numbers (comma or space separated)
        if elem.text:
            raw = str(elem.text).strip()
            if raw:
                # Try comma-separated first
                if ',' in raw:
                    parts = [p.strip() for p in raw.split(',')]
                else:
                    parts = raw.split()
                if len(parts) == 3:
                    x = _to_float(parts[0])
                    y = _to_float(parts[1])
                    z = _to_float(parts[2])
                    if None not in (x, y, z):
                        return (x, y, z)

        # Case 4: nested element <coord x="" y="" z=""> or similar common naming
        for tag in ('coord', 'center', 'coords', 'position'):
            sub = elem.find(tag)
            if sub is not None:
                # recur once on the subelement
                result = XMLStorage.getcoordinates(sub, '.')
                if result is not None:
                    return result

        return None
