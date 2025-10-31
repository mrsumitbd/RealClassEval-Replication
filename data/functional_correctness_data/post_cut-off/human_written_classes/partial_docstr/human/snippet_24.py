import jwt
import json
from typing import Tuple, Optional
from datetime import datetime, timedelta, timezone
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import time

class AuthToken:

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
        self.encryption_key = self._derive_key(32)

    def _derive_key(self, length: int) -> bytes:
        """派生固定长度的密钥"""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        salt = b'fixed_salt_placeholder'
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt, iterations=100000, backend=default_backend())
        return kdf.derive(self.secret_key)

    def _encrypt_payload(self, payload: dict) -> str:
        """使用AES-GCM加密整个payload"""
        payload_json = json.dumps(payload)
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(payload_json.encode()) + encryptor.finalize()
        tag = encryptor.tag
        encrypted_data = iv + ciphertext + tag
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def _decrypt_payload(self, encrypted_data: str) -> dict:
        """解密AES-GCM加密的payload"""
        data = base64.urlsafe_b64decode(encrypted_data.encode())
        iv = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return json.loads(plaintext.decode())

    def generate_token(self, device_id: str) -> str:
        """
        生成JWT token
        :param device_id: 设备ID
        :return: JWT token字符串
        """
        expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = {'device_id': device_id, 'exp': expire_time.timestamp()}
        encrypted_payload = self._encrypt_payload(payload)
        outer_payload = {'data': encrypted_payload}
        token = jwt.encode(outer_payload, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        验证token
        :param token: JWT token字符串
        :return: (是否有效, 设备ID)
        """
        try:
            outer_payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            inner_payload = self._decrypt_payload(outer_payload['data'])
            if inner_payload['exp'] < time.time():
                return (False, None)
            return (True, inner_payload['device_id'])
        except jwt.InvalidTokenError:
            return (False, None)
        except json.JSONDecodeError:
            return (False, None)
        except Exception as e:
            print(f'Token verification failed: {str(e)}')
            return (False, None)