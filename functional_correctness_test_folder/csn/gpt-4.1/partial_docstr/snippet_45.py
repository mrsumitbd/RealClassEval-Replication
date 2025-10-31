
class TokenStoreBase:
    '''Token store base class'''

    def __init__(self, token_collection='default'):
        '''Instantiate instance variables
        Args:
            token_collection (str): The name of the token collection to use. This may be
                used to store different token collections for different client programs.
        '''
        self.token_collection = token_collection
        self._store = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        key = (music_service_id, household_id)
        self._store[key] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        key = (music_service_id, household_id)
        return self._store.get(key, None)

    def has_token(self, music_service_id, household_id):
        '''Return True if a token is stored for the music service and household ID'''
        key = (music_service_id, household_id)
        return key in self._store
