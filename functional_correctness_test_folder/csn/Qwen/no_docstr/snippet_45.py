
class TokenStoreBase:

    def __init__(self, token_collection='default'):
        self.token_collection = token_collection
        self.tokens = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        if music_service_id not in self.tokens:
            self.tokens[music_service_id] = {}
        self.tokens[music_service_id][household_id] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        return self.tokens.get(music_service_id, {}).get(household_id, None)

    def has_token(self, music_service_id, household_id):
        return music_service_id in self.tokens and household_id in self.tokens[music_service_id]
