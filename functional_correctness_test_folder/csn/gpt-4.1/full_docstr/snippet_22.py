
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
        # Example validation: check if transaction has 'id' and 'inputs'
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary.")
        if 'id' not in transaction:
            raise ValueError("Transaction missing 'id'.")
        if 'inputs' not in transaction:
            raise ValueError("Transaction missing 'inputs'.")
        if not isinstance(transaction['inputs'], list):
            raise ValueError("'inputs' must be a list.")
        # Optionally, check if transaction id is unique in bigchaindb
        if hasattr(bigchaindb, 'get_transaction'):
            if bigchaindb.get_transaction(transaction['id']) is not None:
                raise ValueError("Transaction with this id already exists.")
        return True

    @staticmethod
    def validate_block(bigchaindb, block):
        '''See :meth:`bigchaindb.models.Block.validate` for documentation.'''
        # Example validation: check if block has 'height' and 'transactions'
        if not isinstance(block, dict):
            raise ValueError("Block must be a dictionary.")
        if 'height' not in block:
            raise ValueError("Block missing 'height'.")
        if 'transactions' not in block:
            raise ValueError("Block missing 'transactions'.")
        if not isinstance(block['transactions'], list):
            raise ValueError("'transactions' must be a list.")
        # Optionally, validate each transaction in the block
        for tx in block['transactions']:
            BaseValidationRules.validate_transaction(bigchaindb, tx)
        return True
