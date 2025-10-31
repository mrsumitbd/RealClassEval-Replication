class SwitchState:
    ON = True
    OFF = False

    @staticmethod
    def to_state(string):
        return SwitchState.ON if string == 'ON' else SwitchState.OFF

    @staticmethod
    def to_string(state):
        return 'ON' if state else 'OFF'