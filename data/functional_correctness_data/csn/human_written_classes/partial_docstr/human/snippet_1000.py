from clkhash.field_formats import FieldSpec, spec_from_json_dict, InvalidSchemaError
from typing import Any, Dict, Hashable, Optional, Sequence, Text, TextIO
from clkhash.key_derivation import DEFAULT_KEY_SIZE as DEFAULT_KDF_KEY_SIZE

class Schema:
    """Linkage Schema which describes how to encode plaintext identifiers.

    :ivar fields: the features or field definitions
    :ivar int l: The length of the resulting encoding in bits. This is the length after XOR folding.
    :ivar int xor_folds: The number of XOR folds to perform on the hash.
    :ivar str kdf_type: The key derivation function to use. Currently,
        the only permitted value is 'HKDF'.
    :ivar str kdf_hash: The hash function to use in key derivation. The
        options are 'SHA256' and 'SHA512'.
    :ivar bytes kdf_info: The info for key derivation. See documentation
        of :func:`key_derivation.hkdf` for details.
    :ivar bytes kdf_salt: The salt for key derivation. See documentation
        of :func:`key_derivation.hkdf` for details.
    :ivar int kdf_key_size: The size of the derived keys in bytes.
    """

    def __init__(self, fields: Sequence[FieldSpec], l: int, xor_folds: int=0, kdf_type: str='HKDF', kdf_hash: str='SHA256', kdf_info: Optional[bytes]=None, kdf_salt: Optional[bytes]=None, kdf_key_size: int=DEFAULT_KDF_KEY_SIZE) -> None:
        self.fields = fields
        self.l = l
        self.xor_folds = xor_folds
        self.kdf_type = kdf_type
        self.kdf_type = kdf_type
        self.kdf_hash = kdf_hash
        self.kdf_info = kdf_info
        self.kdf_salt = kdf_salt
        self.kdf_key_size = kdf_key_size

    def __repr__(self):
        return f'<Schema (v3): {len(self.fields)} fields>'