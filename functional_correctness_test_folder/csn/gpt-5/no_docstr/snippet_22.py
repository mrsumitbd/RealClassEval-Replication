class BaseValidationRules:
    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        # Basic structural validation for a transaction-like mapping
        if not isinstance(transaction, dict):
            return False

        required_keys = {'id', 'operation', 'inputs', 'outputs', 'version'}
        if not required_keys.issubset(transaction.keys()):
            return False

        # Validate types of some standard fields
        if not isinstance(transaction['id'], str) or not transaction['id']:
            return False

        if not isinstance(transaction['operation'], str) or not transaction['operation']:
            return False

        if not isinstance(transaction['version'], (str, int)):
            return False

        if not isinstance(transaction['inputs'], list):
            return False

        if not isinstance(transaction['outputs'], list) or not transaction['outputs']:
            return False

        return True

    @staticmethod
    def validate_block(bigchaindb, block):
        # Basic structural validation for a block-like mapping
        if not isinstance(block, dict):
            return False

        # Try different common shapes for blocks
        txs = None
        if 'block' in block and isinstance(block['block'], dict):
            inner = block['block']
            txs = inner.get('transactions', None)
        elif 'transactions' in block:
            txs = block.get('transactions', None)

        if not isinstance(txs, list) or len(txs) == 0:
            return False

        # Validate each transaction in the block
        for tx in txs:
            if not BaseValidationRules.validate_transaction(bigchaindb, tx):
                return False

        return True
