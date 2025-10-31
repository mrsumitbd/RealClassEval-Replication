class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        '''See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        '''
        return transaction.validate(bigchaindb)

    @staticmethod
    def validate_block(bigchaindb, block):
        return block.validate(bigchaindb)
