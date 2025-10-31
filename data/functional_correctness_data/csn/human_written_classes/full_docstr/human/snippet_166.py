from mapchete.path import MPath

class OutputSTACMixin:
    """Adds STAC related features."""
    path: MPath
    output_params: dict

    @property
    def stac_path(self) -> MPath:
        """Return path to STAC JSON file."""
        return self.path / f'{self.stac_item_id}.json'

    @property
    def stac_item_id(self) -> str:
        """
        Return STAC item ID according to configuration.

        Defaults to path basename.
        """
        return self.output_params.get('stac', {}).get('id') or self.path.stem

    @property
    def stac_item_metadata(self):
        """Custom STAC metadata."""
        return self.output_params.get('stac', {})

    @property
    def stac_asset_type(self):
        """Asset MIME type."""
        raise ValueError('no MIME type set for this output')