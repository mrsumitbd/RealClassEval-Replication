class TokenStoreBase:

    def __init__(self, token_collection='default'):
        self.token_collection = token_collection
        self._tokens = {}

    def save_token_pair(self, music_service_id, household_id, token_pair):
        if music_service_id is None or household_id is None:
            raise ValueError(
                "music_service_id and household_id must be provided")
        self._tokens[(music_service_id, household_id)] = token_pair

    def load_token_pair(self, music_service_id, household_id):
        if music_service_id is None or household_id is None:
            raise ValueError(
                "music_service_id and household_id must be provided")
        return self._tokens.get((music_service_id, household_id))

    def has_token(self, music_service_id, household_id):
        if music_service_id is None or household_id is None:
            return False
        return (music_service_id, household_id) in self._tokens
