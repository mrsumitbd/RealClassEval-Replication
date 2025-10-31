
class TokenStoreBase:
    '''Token store base class'''

    # Class‑level storage for all collections
    _collections = {}

    def __init__(self, token_collection='default'):
        '''Instantiate instance variables
        Args:
            token_collection (str): The name of the token collection to use. This may be
                used to store different token collections for different client programs.
        '''
        self.token_collection = token_collection
        # Ensure the collection exists
        if token_collection not in self._collections:
            self._collections[token_collection] = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        '''Save a token value pair (token, key) which is a 2 item sequence'''
        if not isinstance(token_pair, (list, tuple)) or len(token_pair) != 2:
            raise ValueError('token_pair must be a 2‑item sequence')
        key = (music_service_id, household_id)
        self._collections[self.token_collection][key] = tuple(token_pair)

    def load_token_pair(self, music_service_id, household_id):
        '''Load a token pair (token, key) which is a 2 item sequence'''
        key = (music_service_id, household_id)
        return self._collections[self.token_collection].get(key)

    def has_token(self, music_service_id, household_id):
        '''Return True if a token is stored for the music service and household ID'''
        key = (music_service_id, household_id)
        return key in self._collections[self.token_collection]
