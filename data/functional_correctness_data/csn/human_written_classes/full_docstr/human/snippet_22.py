class BaseValidationRules:
    """Base validation rules for BigchainDB.

    A validation plugin must expose a class inheriting from this one via an entry_point.

    All methods listed below must be implemented.
    """

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        """See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        """
        return transaction.validate(bigchaindb)

    @staticmethod
    def validate_block(bigchaindb, block):
        """See :meth:`bigchaindb.models.Block.validate` for documentation."""
        return block.validate(bigchaindb)