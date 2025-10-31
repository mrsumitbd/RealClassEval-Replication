class XMLStorage:
    @staticmethod
    def _get_root(tree):
        try:
            # ElementTree
            return tree.getroot()
        except AttributeError:
            # Already an Element
            return tree

    @staticmethod
    def _convert_value(value, force_string=False):
        if value is None:
            return None
        s = value.strip()
        if force_string:
            return s
        # booleans
        low = s.lower()
        if low in ("true", "yes", "on"):
            return True
        if low in ("false", "no", "off"):
            return False
        # int
        try:
            if s.isdigit() or (s.startswith(('+', '-')) and s[1:].isdigit()):
                return int(s)
        except Exception:
            pass
        # float
        try:
            return float(s)
        except Exception:
            pass
        return s

    @staticmethod
    def _split_path_attr(location):
        # support path ending with /@attr or .../@attr
        if not location:
            return location, None
        if "/@" in location:
            idx = location.rfind("/@")
            return location[:idx], location[idx + 2:]
        # also support last-segment @attr like "node@id"
        if "@" in location and "/@" not in location:
            # only treat as attribute if it's in the last segment
            parts = location.split("/")
            last = parts[-1]
            if last.startswith("@"):
                # path like "path/@attr"
                return "/".join(parts[:-1]), last[1:]
            if "@" in last:
                seg, attr = last.split("@", 1)
                parts[-1] = seg
                return "/".join([p for p in parts if p]), attr
        return location, None

    @staticmethod
    def getdata(tree, location, force_string=False):
        root = XMLStorage._get_root(tree)
        if not location:
            return None

        path, attr = XMLStorage._split_path_attr(location)

        try:
            elems = root.findall(path) if path else [root]
        except SyntaxError:
            # fallback: try direct children lookup simple tags
            elems = []
            cur = [root]
            for seg in [s for s in path.split("/") if s]:
                nxt = []
                for e in cur:
                    nxt.extend(list(e.findall(seg)))
                cur = nxt
            elems = cur

        results = []
        for e in elems:
            if attr:
                val = e.get(attr)
            else:
                # if element has text, use it; otherwise, if it has a single child with text, try that
                val = e.text if e.text is not None else None
                if (val is None or not str(val).strip()) and len(list(e)) == 1:
                    child = list(e)[0]
                    if child is not None and child.text:
                        val = child.text
            results.append(XMLStorage._convert_value(val, force_string))

        if not results:
            return None
        # If any list elements are None and others exist, keep them as None to preserve positions
        # If single result, return scalar
        if len(results) == 1:
            return results[0]
        return results

    @staticmethod
    def getcoordinates(tree, location):
        root = XMLStorage._get_root(tree)
        if not location:
            return None

        try:
            elems = root.findall(location)
        except SyntaxError:
            elems = []
            cur = [root]
            for seg in [s for s in location.split("/") if s]:
                nxt = []
                for e in cur:
                    nxt.extend(list(e.findall(seg)))
                cur = nxt
            elems = cur

        coords = []

        def parse_pair(e):
            # Try attributes first
            lat = e.get("lat") or e.get("latitude") or e.get("y")
            lon = e.get("lon") or e.get("long") or e.get(
                "longitude") or e.get("x")
            # If not attributes, try child elements
            if lat is None:
                lat_elem = e.find("lat") or e.find("latitude") or e.find("y")
                lat = lat_elem.text if lat_elem is not None else None
            if lon is None:
                lon_elem = e.find("lon") or e.find(
                    "long") or e.find("longitude") or e.find("x")
                lon = lon_elem.text if lon_elem is not None else None
            # Some formats store coordinates as single text "lat,lon" or "lon,lat"
            if (lat is None or lon is None) and e.text:
                txt = e.text.strip()
                if "," in txt:
                    a, b = [t.strip() for t in txt.split(",", 1)]
                    # heuristics: if absolute value of first > 90, it's lon,lat
                    try:
                        fa = float(a)
                        fb = float(b)
                        if abs(fa) > 90 and abs(fb) <= 90:
                            lon, lat = a, b
                        elif abs(fb) > 90 and abs(fa) <= 90:
                            lat, lon = a, b
                        else:
                            # default to lat,lon
                            lat, lon = a, b
                    except Exception:
                        pass

            if lat is None or lon is None:
                return None
            try:
                return (float(lat), float(lon))
            except Exception:
                return None

        for e in elems:
            pair = parse_pair(e)
            if pair is not None:
                coords.append(pair)

        if not coords:
            return None
        if len(coords) == 1:
            return coords[0]
        return coords
