
class TokenStoreBase:

    def __init__(self, token_collection='default'):
        self.token_collection = token_collection
        self._store = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        key = (music_service_id, household_id)
        self._store[key] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        key = (music_service_id, household_id)
        return self._store.get(key, None)

    def has_token(self, music_service_id, household_id):
        key = (music_service_id, household_id)
        return key in self._store
