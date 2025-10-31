
class BaseValidationRules:

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        # Example validation: Check if transaction ID is unique
        if bigchaindb.get_transaction(transaction['id']):
            return False
        # Example validation: Check if transaction inputs are valid
        for input_ in transaction['inputs']:
            if not bigchaindb.get_unspent_output(input_['fulfills']['output_index'], input_['fulfills']['transaction_id']):
                return False
        return True

    @staticmethod
    def validate_block(bigchaindb, block):
        # Example validation: Check if block index is sequential
        if block['index'] != bigchaindb.get_latest_block()['index'] + 1:
            return False
        # Example validation: Check if block previous hash matches the latest block hash
        if block['previous_block'] != bigchaindb.get_latest_block()['id']:
            return False
        # Example validation: Validate each transaction in the block
        for transaction in block['transactions']:
            if not BaseValidationRules.validate_transaction(bigchaindb, transaction):
                return False
        return True
