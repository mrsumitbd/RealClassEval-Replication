class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''

    @staticmethod
    def _root(tree):
        try:
            return tree.getroot()
        except AttributeError:
            return tree

    @staticmethod
    def _coerce_value(text, force_string=False):
        if text is None:
            return None
        s = str(text).strip()
        if s == "":
            return None
        if force_string:
            return s
        lower = s.lower()
        if lower in {"true", "yes"}:
            return True
        if lower in {"false", "no"}:
            return False
        # Int
        try:
            if s.isdigit() or (s.startswith(("+", "-")) and s[1:].isdigit()):
                return int(s)
        except Exception:
            pass
        # Float
        try:
            return float(s)
        except Exception:
            pass
        return s

    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        root = XMLStorage._root(tree)

        # Support attribute selector at end: path/@attr
        attr_name = None
        attr_path = None
        if "/@" in location:
            attr_path, attr_name = location.rsplit("/@", 1)

        try:
            if attr_name:
                elems = list(root.findall(attr_path))
                if not elems:
                    return None
                values = [e.get(attr_name) for e in elems]
                values = [XMLStorage._coerce_value(
                    v, force_string) for v in values]
            else:
                elems = list(root.findall(location))
                if not elems:
                    return None
                values = [XMLStorage._coerce_value(
                    e.text, force_string) for e in elems]
        except Exception:
            return None

        # Collapse singletons
        if len(values) == 1:
            return values[0]
        return values

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        import re

        root = XMLStorage._root(tree)

        try:
            elems = list(root.findall(location))
        except Exception:
            return None
        if not elems:
            return None

        def parse_coords(elem):
            # 1) Attributes x,y,z
            for keyset in (("x", "y", "z"), ("X", "Y", "Z")):
                if all(k in elem.attrib for k in keyset):
                    try:
                        return (
                            float(elem.attrib[keyset[0]]),
                            float(elem.attrib[keyset[1]]),
                            float(elem.attrib[keyset[2]]),
                        )
                    except Exception:
                        pass
            # 2) Child elements <x>,<y>,<z>

            def child_text(name):
                c = elem.find(name)
                return None if c is None else c.text
            for names in (("x", "y", "z"), ("X", "Y", "Z")):
                xt, yt, zt = child_text(names[0]), child_text(
                    names[1]), child_text(names[2])
                if xt is not None and yt is not None and zt is not None:
                    try:
                        return (float(xt), float(yt), float(zt))
                    except Exception:
                        pass
            # 3) Text with three numbers
            txt = elem.text.strip() if elem.text else ""
            if txt:
                nums = re.findall(
                    r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", txt.replace(",", " "))
                if len(nums) >= 3:
                    try:
                        return (float(nums[0]), float(nums[1]), float(nums[2]))
                    except Exception:
                        pass
            return None

        coords_list = [parse_coords(e) for e in elems]
        coords_list = [c for c in coords_list if c is not None]

        if not coords_list:
            return None
        if len(elems) == 1:
            return coords_list[0]
        return coords_list
