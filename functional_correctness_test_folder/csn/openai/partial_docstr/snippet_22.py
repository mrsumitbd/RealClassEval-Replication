
class BaseValidationRules:
    """
    Basic validation rules for transactions and blocks.
    These rules simply invoke the built‑in `validate` methods of the
    transaction and block objects.  Any exception raised during
    validation is caught and treated as a validation failure.
    """

    @staticmethod
    def validate_transaction(bigchaindb, transaction):
        """
        Validate a transaction against the current state of the
        BigchainDB instance.

        Parameters
        ----------
        bigchaindb : object
            The BigchainDB instance (unused in this basic rule but
            kept for API compatibility).
        transaction : object
            The transaction object to validate.  It must expose a
            ``validate`` method.

        Returns
        -------
        bool
            ``True`` if the transaction validates successfully,
            ``False`` otherwise.
        """
        try:
            # The transaction's own validate method performs all checks.
            transaction.validate()
            return True
        except Exception:
            return False

    @staticmethod
    def validate_block(bigchaindb, block):
        """
        Validate a block against the current state of the
        BigchainDB instance.

        Parameters
        ----------
        bigchaindb : object
            The BigchainDB instance (unused in this basic rule but
            kept for API compatibility).
        block : object
            The block object to validate.  It must expose a
            ``validate`` method.

        Returns
        -------
        bool
            ``True`` if the block validates successfully,
            ``False`` otherwise.
        """
        try:
            # The block's own validate method performs all checks.
            block.validate()
            return True
        except Exception:
            return False
