class LocalId:
    """
    Class for local ids for non-persisted xblocks (which can have hardcoded block_ids if necessary)
    """

    def __init__(self, block_id: str | None=None):
        self.block_id = block_id
        super().__init__()

    def __str__(self):
        identifier = self.block_id or id(self)
        return f'localid_{identifier}'