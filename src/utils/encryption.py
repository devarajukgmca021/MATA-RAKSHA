import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

class EncryptionManager:
    def __init__(self):
        encryption_key = os.environ.get('ENCRYPTION_KEY')
        
        if not encryption_key:
            raise ValueError(
                "ENCRYPTION_KEY environment variable is required for secure key storage. "
                "Set it to a strong, random 32+ character string. "
                "Example: export ENCRYPTION_KEY='your-strong-random-key-here'"
            )
        
        if len(encryption_key) < 32:
            raise ValueError(
                "ENCRYPTION_KEY must be at least 32 characters long for security. "
                f"Current length: {len(encryption_key)}"
            )
        
        self.key = PBKDF2(encryption_key, b'mata-raksha-salt', dkLen=32, count=100000)
    
    def encrypt(self, plaintext):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        nonce = cipher.nonce
        combined = nonce + tag + ciphertext
        
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt(self, encrypted_data):
        if isinstance(encrypted_data, str):
            encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
        
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        return plaintext.decode('utf-8')
