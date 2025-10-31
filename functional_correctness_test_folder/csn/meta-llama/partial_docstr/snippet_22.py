
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        '''See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        '''
        return transaction.validate(bigchaindb)

    @staticmethod
    def validate_block(bigchaindb, block):
        if not bigchaindb.has_previous_vote(block.id, block.election_index):
            return block.validate(bigchaindb)
        else:
            return block
