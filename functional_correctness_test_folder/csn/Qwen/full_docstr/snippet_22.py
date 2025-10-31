
class BaseValidationRules:
    '''Base validation rules for BigchainDB.
    A validation plugin must expose a class inheriting from this one via an entry_point.
    All methods listed below must be implemented.
    '''
    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        '''See :meth:`bigchaindb.models.Transaction.validate`
        for documentation.
        '''
        # Implement transaction validation logic here
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
        '''See :meth:`bigchaindb.models.Block.validate` for documentation.'''
        # Implement block validation logic here
        if not block:
            return False
        if not block.get('id'):
            return False
        if not block.get('timestamp'):
            return False
        if not block.get('transactions'):
            return False
        if not block.get('node_pubkey'):
            return False
        if not block.get('voters'):
            return False
        if not block.get('height'):
            return False
        return True
