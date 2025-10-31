
class TokenStoreBase:
    '''Token store base class'''

    def __init__(self, token_collection='default'):
        '''Instantiate instance variables
        Args:
            token_collection (str): The name of the token collection to use. This may be
                used to store different token collections for different client programs.
        '''
        self.token_collection = token_collection
        # Internal storage: {collection_name: {(music_service_id, household_id): token_pair}}
        self._store = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        '''Store a token pair for the given music service and household ID.'''
        collection = self._store.setdefault(self.token_collection, {})
        collection[(music_service_id, household_id)] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        '''Retrieve the token pair for the given music service and household ID.
        Returns:
            The stored token_pair or None if not found.
        '''
        collection = self._store.get(self.token_collection, {})
        return collection.get((music_service_id, household_id))

    def has_token(self, music_service_id, household_id):
        '''Return True if a token is stored for the music service and household ID'''
        collection = self._store.get(self.token_collection, {})
        return (music_service_id, household_id) in collection
