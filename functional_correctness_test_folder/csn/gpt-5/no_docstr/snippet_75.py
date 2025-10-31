class Geometry:
    def __init__(self, geom_type, coordinates, bbox=None):
        self.type = geom_type
        self.coordinates = coordinates
        self._validate()
        self.bbox = bbox if bbox is not None else self._compute_bbox()

    def _validate(self):
        if not isinstance(self.type, str) or not self.type:
            raise ValueError("Geometry type must be a non-empty string.")
        if self.type not in {
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
            "GeometryCollection",
        }:
            raise ValueError(f"Unsupported geometry type: {self.type}")

        if self.type == "GeometryCollection":
            if not isinstance(self.coordinates, list):
                raise ValueError(
                    "GeometryCollection must be a list of geometries.")
            for geom in self.coordinates:
                if not isinstance(geom, dict) or "type" not in geom:
                    raise ValueError(
                        "Each geometry in GeometryCollection must be a dict with a 'type'.")
        else:
            if self.coordinates is None:
                raise ValueError("Coordinates must not be None.")
            # Basic shape checks for common types
            if self.type == "Point":
                self._validate_position(self.coordinates)
            elif self.type == "MultiPoint":
                self._validate_positions(self.coordinates)
            elif self.type == "LineString":
                self._validate_positions(self.coordinates, min_len=2)
            elif self.type == "MultiLineString":
                if not isinstance(self.coordinates, list) or not self.coordinates:
                    raise ValueError(
                        "MultiLineString must be a non-empty list of LineStrings.")
                for ls in self.coordinates:
                    self._validate_positions(ls, min_len=2)
            elif self.type == "Polygon":
                self._validate_polygon(self.coordinates)
            elif self.type == "MultiPolygon":
                if not isinstance(self.coordinates, list) or not self.coordinates:
                    raise ValueError(
                        "MultiPolygon must be a non-empty list of Polygons.")
                for poly in self.coordinates:
                    self._validate_polygon(poly)

    def _validate_position(self, pos):
        if (
            not isinstance(pos, (list, tuple))
            or len(pos) < 2
            or not all(isinstance(n, (int, float)) for n in pos[:2])
        ):
            raise ValueError(
                "Position must be a list/tuple of at least two numbers [x, y, ...].")

    def _validate_positions(self, positions, min_len=1):
        if not isinstance(positions, list) or len(positions) < min_len:
            raise ValueError(
                f"Positions must be a list with at least {min_len} positions.")
        for p in positions:
            self._validate_position(p)

    def _validate_linear_ring(self, ring):
        self._validate_positions(ring, min_len=4)
        if ring[0][:2] != ring[-1][:2]:
            raise ValueError(
                "LinearRing must be closed (first and last positions must be equal).")

    def _validate_polygon(self, coords):
        if not isinstance(coords, list) or not coords:
            raise ValueError(
                "Polygon must be a non-empty list of LinearRings.")
        for ring in coords:
            self._validate_linear_ring(ring)

    def _iter_positions(self, coords=None):
        if coords is None:
            coords = self.coordinates
        if self.type == "Point":
            yield coords
        elif self.type in ("MultiPoint", "LineString"):
            for p in coords:
                yield p
        elif self.type in ("MultiLineString", "Polygon"):
            for part in coords:
                for p in part:
                    yield p
        elif self.type == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    for p in ring:
                        yield p
        elif self.type == "GeometryCollection":
            for geom in coords:
                if not isinstance(geom, dict):
                    continue
                gtype = geom.get("type")
                gcoords = geom.get("coordinates")
                if gtype == "Point":
                    if gcoords is not None:
                        yield gcoords
                elif gtype in ("MultiPoint", "LineString"):
                    for p in (gcoords or []):
                        yield p
                elif gtype in ("MultiLineString", "Polygon"):
                    for part in (gcoords or []):
                        for p in part:
                            yield p
                elif gtype == "MultiPolygon":
                    for poly in (gcoords or []):
                        for ring in poly:
                            for p in ring:
                                yield p

    def _compute_bbox(self):
        xs = []
        ys = []
        for pos in self._iter_positions():
            if (
                isinstance(pos, (list, tuple))
                and len(pos) >= 2
                and isinstance(pos[0], (int, float))
                and isinstance(pos[1], (int, float))
            ):
                xs.append(pos[0])
                ys.append(pos[1])
        if not xs or not ys:
            return None
        return [min(xs), min(ys), max(xs), max(ys)]

    def geojson(self):
        obj = {"type": self.type}
        if self.type == "GeometryCollection":
            obj["geometries"] = self.coordinates
        else:
            obj["coordinates"] = self.coordinates
        if self.bbox is not None:
            obj["bbox"] = list(self.bbox)
        return obj

    def to_dict(self):
        d = {
            "type": self.type,
            "coordinates": self.coordinates,
        }
        if self.bbox is not None:
            d["bbox"] = list(self.bbox)
        return d
