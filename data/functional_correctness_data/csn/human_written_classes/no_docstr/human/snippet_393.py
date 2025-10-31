from pyportify.serializers import Track

class SpotifyQuery:

    def __init__(self, i, sp_playlist_uri, sp_track, track_count):
        self.track = Track.from_spotify(sp_track.get('track', {}))
        self.i = i
        self.playlist_uri = sp_playlist_uri
        self.track_count = track_count

    def search_query(self):
        track = self.track
        if not track.name or not track.artist:
            return None
        if track.artist:
            search_query = '{0} - {1}'.format(track.artist, track.name)
        else:
            search_query = '{0}'.format(track.name)
        return search_query