class AnswerMachine:

    def __init__(self, always_yes=False, confirmed=False):
        self._always_yes = always_yes
        self._confirmed = confirmed

    def get(self, msg):
        if self._always_yes:
            return True
        if self._confirmed:
            print(msg)
            return True
        while True:
            res = input(f'{msg} (y/n/a)? ')
            if res == 'a':
                self._confirmed = True
                return True
            if res == 'y':
                return True
            if res == 'n':
                return False