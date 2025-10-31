
class TorConfigType:

    def parse(self, s):
        # For this example, let's assume Tor config values can be:
        # - Boolean: "1"/"0", "yes"/"no", "true"/"false"
        # - Integer: "80", "9050"
        # - String: any other value
        s = s.strip()
        lower = s.lower()
        if lower in ("1", "yes", "true"):
            return True
        elif lower in ("0", "no", "false"):
            return False
        try:
            return int(s)
        except ValueError:
            return s

    def validate(self, s, instance, name):
        # For this example, let's just check that s is not empty or None
        if s is None or (isinstance(s, str) and not s.strip()):
            raise ValueError(f"Config value for '{name}' cannot be empty")
        # Optionally, you could add more validation based on name
        return True
