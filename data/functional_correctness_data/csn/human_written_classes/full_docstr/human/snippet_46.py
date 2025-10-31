class ShareClass:
    """Base class for supported services."""

    def canonical_uri(self, uri):
        """Recognize a share link and return its canonical representation.

        Args:
            uri (str): A URI like "https://tidal.com/browse/album/157273956".

        Returns:
            str: The canonical URI or None if not recognized.
        """
        raise NotImplementedError

    def service_number(self):
        """Return the service number.

        Returns:
            int: A number identifying the supported music service.
        """
        raise NotImplementedError

    @staticmethod
    def magic():
        """Return magic.

        Returns:
            dict: Magic prefix/key/class values for each share type.
        """
        return {'album': {'prefix': 'x-rincon-cpcontainer:1004206c', 'key': '00040000', 'class': 'object.container.album.musicAlbum'}, 'episode': {'prefix': '', 'key': '00032020', 'class': 'object.item.audioItem.musicTrack'}, 'track': {'prefix': '', 'key': '00032020', 'class': 'object.item.audioItem.musicTrack'}, 'show': {'prefix': 'x-rincon-cpcontainer:1006206c', 'key': '1006206c', 'class': 'object.container.playlistContainer'}, 'song': {'prefix': '', 'key': '10032020', 'class': 'object.item.audioItem.musicTrack'}, 'playlist': {'prefix': 'x-rincon-cpcontainer:1006206c', 'key': '1006206c', 'class': 'object.container.playlistContainer'}}

    def extract(self, uri):
        """Extract the share type and encoded URI from a share link.

        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        """
        raise NotImplementedError