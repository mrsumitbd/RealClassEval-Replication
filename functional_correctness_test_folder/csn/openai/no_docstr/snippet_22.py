
import json
import hashlib
from typing import Any, Dict, List, Optional


class BaseValidationRules:
    @staticmethod
    def _hash(data: Any) -> str:
        """Return a SHA-256 hex digest of the JSON representation of *data*."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def _hash_pair(a: str, b: str) -> str:
        """Return a SHA-256 hex digest of the concatenation of two hex strings."""
        return hashlib.sha256((a + b).encode()).hexdigest()

    @staticmethod
    def _merkle_root(hashes: List[str]) -> str:
        """Compute the merkle root of a list of hex string hashes."""
        if not hashes:
            return ""
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                new_hashes.append(BaseValidationRules._hash_pair(
                    hashes[i], hashes[i + 1]))
            hashes = new_hashes
        return hashes[0]

    @staticmethod
    def validate_transaction(bigchaindb, transaction: Dict[str, Any]) -> bool:
        """
        Validate a BigchainDB transaction.

        Raises:
            ValueError: If the transaction is invalid.
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")

        required_keys = {"id", "operation", "data",
                         "metadata", "signatures", "outputs", "inputs"}
        missing = required_keys - transaction.keys()
        if missing:
            raise ValueError(f"Missing transaction keys: {missing}")

        tx_id = transaction["id"]
        if not isinstance(tx_id, str):
            raise ValueError("Transaction 'id' must be a string")

        operation = transaction["operation"]
        if operation not in {"CREATE", "TRANSFER", "REVOKE"}:
            raise ValueError(f"Unsupported operation: {operation}")

        if not isinstance(transaction["data"], dict):
            raise ValueError("Transaction 'data' must be a dictionary")

        if not isinstance(transaction["metadata"], dict):
            raise ValueError("Transaction 'metadata' must be a dictionary")

        signatures = transaction["signatures"]
        if not isinstance(signatures, list):
            raise ValueError("Transaction 'signatures' must be a list")

        outputs = transaction["outputs"]
        if not isinstance(outputs, list):
            raise ValueError("Transaction 'outputs' must be a list")

        inputs = transaction["inputs"]
        if not isinstance(inputs, list):
            raise ValueError("Transaction 'inputs' must be a list")

        # Validate signatures
        for sig in signatures:
            if not isinstance(sig, dict):
                raise ValueError("Each signature must be a dictionary")
            for key in ("public_key", "signature", "type", "output_index", "input_index", "output"):
                if key not in sig:
                    raise ValueError(f"Signature missing key: {key}")
            if not isinstance(sig["output_index"], int) or sig["output_index"] >= len(outputs):
                raise ValueError("Signature 'output_index' out of range")

        # Validate inputs
        for inp in inputs:
            if not isinstance(inp, dict):
                raise ValueError("Each input must be a dictionary")
            for key in ("output", "fulfillment", "fulfills", "owners_before"):
                if key not in inp:
                    raise ValueError(f"Input missing key: {key}")

            fulfills = inp["fulfills"]
            if not isinstance(fulfills, dict):
                raise ValueError("Input 'fulfills' must be a dictionary")
            if "transaction_id" not in fulfills or "output_index" not in fulfills:
                raise ValueError("Input 'fulfills' missing required keys")

            prev_tx_id = fulfills["transaction_id"]
            prev_output_index = fulfills["output_index"]

            # Verify referenced transaction exists
            try
