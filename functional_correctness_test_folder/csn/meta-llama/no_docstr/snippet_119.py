
class DummyClass:

    def __init__(self, value):
        self._value = value
        self._result = None

    def run(self):
        self._result = self._value * 2

    @property
    def prop(self):
        return self._result


# Example usage:
if __name__ == "__main__":
    dummy = DummyClass(10)
    print(dummy.prop)  # Output: None
    dummy.run()
    print(dummy.prop)  # Output: 20
