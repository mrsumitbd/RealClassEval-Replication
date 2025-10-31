
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        '''See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        '''
        # Assume bigchaindb.models.Transaction.validate is the reference
        # Here, we call the transaction's validate method, passing bigchaindb
        return transaction.validate(bigchaindb)

    @staticmethod
    def validate_block(bigchaindb, block):
        # Assume block has a validate method that takes bigchaindb as argument
        return block.validate(bigchaindb)
