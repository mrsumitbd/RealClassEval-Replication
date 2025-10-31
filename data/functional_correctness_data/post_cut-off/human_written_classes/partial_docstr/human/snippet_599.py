class SeriesMixin:

    def is_series(self) -> bool:
        """
        Check if this movie title is a series, the main title of a series.
        If True, it means that this is a series, not a movie, not an episode, but the main reference for the series itself, and series details can be found in the self.info_series property.
        """
        return getattr(self, 'kind', None) in SERIES_IDENTIFIERS

    def is_episode(self) -> bool:
        """
        Check if this movie title is an episode of a series.
        If True, means that this is the episode of a series and episode details can be found in the self.info_episode property
        """
        return getattr(self, 'kind', None) in EPISODE_IDENTIFIERS