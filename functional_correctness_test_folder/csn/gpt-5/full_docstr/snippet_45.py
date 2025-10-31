class TokenStoreBase:
    '''Token store base class'''

    def __init__(self, token_collection='default'):
        '''Instantiate instance variables
        Args:
            token_collection (str): The name of the token collection to use. This may be
                used to store different token collections for different client programs.
        '''
        self.token_collection = str(token_collection)
        self._tokens = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        '''Save a token value pair (token, key) which is a 2 item sequence'''
        try:
            token, key = token_pair
        except Exception as exc:
            raise ValueError(
                "token_pair must be a 2-item sequence (token, key)") from exc
        self._tokens[(music_service_id, household_id)] = (token, key)

    def load_token_pair(self, music_service_id, household_id):
        '''Load a token pair (token, key) which is a 2 item sequence'''
        return self._tokens.get((music_service_id, household_id))

    def has_token(self, music_service_id, household_id):
        '''Return True if a token is stored for the music service and household ID'''
        return (music_service_id, household_id) in self._tokens
