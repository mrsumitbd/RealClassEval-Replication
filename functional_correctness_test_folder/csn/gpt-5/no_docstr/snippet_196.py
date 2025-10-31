class Mechanism:

    def __init__(self, mechanism, param=None):
        import copy

        self.name = None
        self.params = {}

        if isinstance(mechanism, Mechanism):
            self.name = mechanism.name
            self.params = copy.deepcopy(mechanism.params)
            if param is not None:
                if not isinstance(param, dict):
                    raise TypeError(
                        "param must be a dict when overriding an existing Mechanism.")
                self.params.update(copy.deepcopy(param))
            return

        if isinstance(mechanism, dict):
            mech_dict = mechanism
            name = mech_dict.get("mechanism") or mech_dict.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError(
                    "Mechanism dict must contain a non-empty 'mechanism' or 'name' string.")

            params = {}
            # Prefer explicit param/params keys; otherwise take remaining keys as params
            if "param" in mech_dict and isinstance(mech_dict["param"], dict):
                params.update(mech_dict["param"])
            elif "params" in mech_dict and isinstance(mech_dict["params"], dict):
                params.update(mech_dict["params"])
            else:
                for k, v in mech_dict.items():
                    if k not in ("mechanism", "name", "param", "params"):
                        params[k] = v

            if param is not None:
                if not isinstance(param, dict):
                    raise TypeError("param must be a dict.")
                params.update(param)

            self.name = name
            self.params = copy.deepcopy(params)
            return

        if isinstance(mechanism, str):
            name = mechanism
            if not name.strip():
                raise ValueError("mechanism name must be a non-empty string.")
            if param is not None and not isinstance(param, dict):
                raise TypeError("param must be a dict.")
            self.name = name
            self.params = copy.deepcopy(param or {})
            return

        raise TypeError("mechanism must be a Mechanism, dict, or str.")

    def to_native(self):
        import copy
        return {
            "mechanism": self.name,
            "param": copy.deepcopy(self.params),
        }
