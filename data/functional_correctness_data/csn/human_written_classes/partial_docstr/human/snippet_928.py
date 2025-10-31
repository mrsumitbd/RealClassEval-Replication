class DeviceError:
    """Container for device-given errors."""

    def __init__(self, error):
        self.error_code, self.error_message = error

    @property
    def error(self):
        """Return user-friendly error message."""
        try:
            errcode = DeviceErrorCode(self.error_code)
            return f'{errcode.name} ({errcode.value}): {self.error_message}'
        except:
            return f'Unknown error {self.error_code}: {self.error_message}'

    def __str__(self):
        return self.error