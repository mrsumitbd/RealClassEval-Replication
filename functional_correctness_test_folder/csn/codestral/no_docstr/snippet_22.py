
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):

        if not isinstance(transaction, dict):
            raise TypeError('Transaction must be a dictionary')

        if 'operation' not in transaction:
            raise ValueError('Transaction must contain an operation')

        if 'inputs' not in transaction:
            raise ValueError('Transaction must contain inputs')

        if 'outputs' not in transaction:
            raise ValueError('Transaction must contain outputs')

        if 'metadata' not in transaction:
            raise ValueError('Transaction must contain metadata')

        if not isinstance(transaction['inputs'], list):
            raise TypeError('Transaction inputs must be a list')

        if not isinstance(transaction['outputs'], list):
            raise TypeError('Transaction outputs must be a list')

        if not isinstance(transaction['metadata'], dict):
            raise TypeError('Transaction metadata must be a dictionary')

        for input in transaction['inputs']:
            if not isinstance(input, dict):
                raise TypeError('Transaction input must be a dictionary')

            if 'fulfills' not in input:
                raise ValueError('Transaction input must contain fulfills')

            if 'fulfills' in input and not isinstance(input['fulfills'], dict):
                raise TypeError(
                    'Transaction input fulfills must be a dictionary')

            if 'fulfills' in input and 'transaction_id' not in input['fulfills']:
                raise ValueError(
                    'Transaction input fulfills must contain transaction_id')

            if 'fulfills' in input and 'output_index' not in input['fulfills']:
                raise ValueError(
                    'Transaction input fulfills must contain output_index')

        for output in transaction['outputs']:
            if not isinstance(output, dict):
                raise TypeError('Transaction output must be a dictionary')

            if 'public_keys' not in output:
                raise ValueError('Transaction output must contain public_keys')

            if not isinstance(output['public_keys'], list):
                raise TypeError(
                    'Transaction output public_keys must be a list')

            if 'condition' not in output:
                raise ValueError('Transaction output must contain condition')

            if not isinstance(output['condition'], dict):
                raise TypeError(
                    'Transaction output condition must be a dictionary')

            if 'details' not in output['condition']:
                raise ValueError(
                    'Transaction output condition must contain details')

            if not isinstance(output['condition']['details'], dict):
                raise TypeError(
                    'Transaction output condition details must be a dictionary')

            if 'type' not in output['condition']:
                raise ValueError(
                    'Transaction output condition must contain type')

            if 'type' not in output['condition']['details']:
                raise ValueError(
                    'Transaction output condition details must contain type')

    @staticmethod
    def validate_block(bigchaindb, block):

        if not isinstance(block, dict):
            raise TypeError('Block must be a dictionary')

        if 'transactions' not in block:
            raise ValueError('Block must contain transactions')

        if not isinstance(block['transactions'], list):
            raise TypeError('Block transactions must be a list')

        if 'node_pubkey' not in block:
            raise ValueError('Block must contain node_pubkey')

        if 'version' not in block:
            raise ValueError('Block must contain version')

        if 'previous_block' not in block:
            raise ValueError('Block must contain previous_block')

        if 'timestamp' not in block:
            raise ValueError('Block must contain timestamp')

        for transaction in block['transactions']:
            BaseValidationRules.validate_transaction(bigchaindb, transaction)
