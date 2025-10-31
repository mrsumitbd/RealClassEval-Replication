
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary.")
        if 'id' not in transaction or 'inputs' not in transaction or 'outputs' not in transaction:
            raise ValueError("Transaction missing required fields.")
        if not isinstance(transaction['inputs'], list) or not isinstance(transaction['outputs'], list):
            raise ValueError(
                "Transaction 'inputs' and 'outputs' must be lists.")
        # Optionally, check if transaction id is unique in bigchaindb
        if hasattr(bigchaindb, 'has_transaction'):
            if bigchaindb.has_transaction(transaction['id']):
                raise ValueError("Transaction with this id already exists.")
        return True

    @staticmethod
    def validate_block(bigchaindb, block):
        if not isinstance(block, dict):
            raise ValueError("Block must be a dictionary.")
        if 'id' not in block or 'transactions' not in block or 'timestamp' not in block:
            raise ValueError("Block missing required fields.")
        if not isinstance(block['transactions'], list):
            raise ValueError("Block 'transactions' must be a list.")
        # Optionally, check if block id is unique in bigchaindb
        if hasattr(bigchaindb, 'has_block'):
            if bigchaindb.has_block(block['id']):
                raise ValueError("Block with this id already exists.")
        # Validate each transaction in the block
        for tx in block['transactions']:
            BaseValidationRules.validate_transaction(bigchaindb, tx)
        return True
