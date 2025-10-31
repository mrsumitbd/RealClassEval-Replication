class RGsolution:

    def __init__(self, fun, scale_min, scale_max):
        if not callable(fun):
            raise TypeError("fun must be callable")
        if not (isinstance(scale_min, (int, float)) and isinstance(scale_max, (int, float))):
            raise TypeError("scale_min and scale_max must be numbers")
        if scale_max <= scale_min:
            raise ValueError("scale_max must be greater than scale_min")
        self.fun = fun
        self.scale_min = float(scale_min)
        self.scale_max = float(scale_max)

    def plotdata(self, key, part='re', scale='log', steps=50):
        if not isinstance(steps, int) or steps < 2:
            raise ValueError("steps must be an integer >= 2")
        if scale not in ('log', 'lin'):
            raise ValueError("scale must be 'log' or 'lin'")
        if part not in ('re', 'im', 'abs'):
            raise ValueError("part must be 're', 'im', or 'abs'")

        if scale == 'log':
            if self.scale_min <= 0:
                raise ValueError("scale_min must be > 0 for log scale")
            ratio = (self.scale_max / self.scale_min) ** (1 / (steps - 1))
            xs = [self.scale_min * (ratio ** i) for i in range(steps)]
        else:
            step = (self.scale_max - self.scale_min) / (steps - 1)
            xs = [self.scale_min + i * step for i in range(steps)]

        ys = []
        for x in xs:
            res = self.fun(x)
            if callable(key):
                val = key(res)
            else:
                try:
                    val = res[key]
                except (TypeError, KeyError):
                    raise KeyError(
                        f"Key {key!r} not found in result at scale {x!r}")
            if part == 're':
                if isinstance(val, complex):
                    ys.append(val.real)
                else:
                    ys.append(float(val))
            elif part == 'im':
                if isinstance(val, complex):
                    ys.append(val.imag)
                else:
                    ys.append(0.0)
            else:
                if isinstance(val, complex):
                    ys.append(abs(val))
                else:
                    ys.append(abs(float(val)))
        return xs, ys

    def plotdata(self, key, part='re', scale='log', steps=50):
        if not isinstance(steps, int) or steps < 2:
            raise ValueError("steps must be an integer >= 2")
        if scale not in ('log', 'lin'):
            raise ValueError("scale must be 'log' or 'lin'")
        if part not in ('re', 'im', 'abs'):
            raise ValueError("part must be 're', 'im', or 'abs'")

        if scale == 'log':
            if self.scale_min <= 0:
                raise ValueError("scale_min must be > 0 for log scale")
            ratio = (self.scale_max / self.scale_min) ** (1 / (steps - 1))
            xs = [self.scale_min * (ratio ** i) for i in range(steps)]
        else:
            step = (self.scale_max - self.scale_min) / (steps - 1)
            xs = [self.scale_min + i * step for i in range(steps)]

        ys = []
        for x in xs:
            res = self.fun(x)
            if callable(key):
                val = key(res)
            else:
                try:
                    val = res[key]
                except (TypeError, KeyError):
                    raise KeyError(
                        f"Key {key!r} not found in result at scale {x!r}")
            if part == 're':
                if isinstance(val, complex):
                    ys.append(val.real)
                else:
                    ys.append(float(val))
            elif part == 'im':
                if isinstance(val, complex):
                    ys.append(val.imag)
                else:
                    ys.append(0.0)
            else:
                if isinstance(val, complex):
                    ys.append(abs(val))
                else:
                    ys.append(abs(float(val)))
        return xs, ys
