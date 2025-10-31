
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        '''See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        '''
        # Example validation logic for a transaction
        if not transaction:
            return False
        if not transaction.get('id'):
            return False
        if not transaction.get('operation'):
            return False
        if not transaction.get('asset'):
            return False
        if not transaction.get('metadata'):
            return False
        if not transaction.get('outputs'):
            return False
        if not transaction.get('inputs'):
            return False
        return True

    @staticmethod
    def validate_block(bigchaindb, block):
        # Example validation logic for a block
        if not block:
            return False
        if not block.get('id'):
            return False
        if not block.get('timestamp'):
            return False
        if not block.get('transactions'):
            return False
        if not block.get('voters'):
            return False
        if not block.get('block_number'):
            return False
        if not block.get('previous_block'):
            return False
        return True
