
class TokenStoreBase:

    def __init__(self, token_collection='default'):
        self.token_collection = token_collection
        self.token_store = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        if music_service_id not in self.token_store:
            self.token_store[music_service_id] = {}
        self.token_store[music_service_id][household_id] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        if music_service_id in self.token_store and household_id in self.token_store[music_service_id]:
            return self.token_store[music_service_id][household_id]
        return None

    def has_token(self, music_service_id, household_id):
        return music_service_id in self.token_store and household_id in self.token_store[music_service_id]
