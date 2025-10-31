
import random
import string


class TraceId:

    def __init__(self):
        '''
        Generate a random trace id.
        '''
        self.id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=16))

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self.id
