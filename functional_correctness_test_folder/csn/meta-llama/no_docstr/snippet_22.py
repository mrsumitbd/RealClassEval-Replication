
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        """Validate a transaction against the current state of the bigchaindb.

        Args:
            bigchaindb: an instance of BigchainDB
            transaction: transaction to validate.

        Returns:
            The transaction if the transaction is valid else it raises an exception
            with the validation error.
        """
        if not isinstance(transaction, dict):
            raise TypeError('Transaction must be a dict')

        if transaction['operation'] not in ['CREATE', 'TRANSFER']:
            raise ValueError('Operation must be either CREATE or TRANSFER')

        # Check if the transaction has the correct structure
        expected_keys = ['id', 'version', 'inputs',
                         'outputs', 'operation', 'metadata', 'asset']
        if set(transaction.keys()) != set(expected_keys):
            raise ValueError('Transaction is missing or has extra keys')

        # Check if the transaction version is supported
        if transaction['version'] not in ['1.0', '2.0']:
            raise ValueError('Transaction version is not supported')

        # Check if the transaction id is valid
        if transaction['id'] != transaction['id']:
            raise ValueError('Transaction id is not valid')

        # Check if the inputs are valid
        if not transaction['inputs']:
            raise ValueError('Transaction inputs cannot be empty')

        # Check if the outputs are valid
        if not transaction['outputs']:
            raise ValueError('Transaction outputs cannot be empty')

        return transaction

    @staticmethod
    def validate_block(bigchaindb, block):
        """Validate a block against the current state of the bigchaindb.

        Args:
            bigchaindb: an instance of BigchainDB
            block: block to validate.

        Returns:
            The block if the block is valid else it raises an exception
            with the validation error.
        """
        if not isinstance(block, dict):
            raise TypeError('Block must be a dict')

        # Check if the block has the correct structure
        expected_keys = ['id', 'block', 'votes']
        if set(block.keys()) != set(expected_keys):
            raise ValueError('Block is missing or has extra keys')

        # Check if the block id is valid
        if block['id'] != block['id']:
            raise ValueError('Block id is not valid')

        # Check if the block contains a valid timestamp
        if not isinstance(block['block']['timestamp'], str):
            raise ValueError('Block timestamp must be a string')

        # Check if the block contains a valid transactions list
        if not isinstance(block['block']['transactions'], list):
            raise ValueError('Block transactions must be a list')

        # Check if all transactions in the block are valid
        for transaction in block['block']['transactions']:
            BaseValidationRules.validate_transaction(bigchaindb, transaction)

        return block
