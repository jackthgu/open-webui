import logging
import os
import json
from typing import Optional, Any, List
from sqlalchemy import text
from open_webui.internal.db import get_db

log = logging.getLogger(__name__)


class PgCrypto:
    def encrypt_data(data: str, password: str) -> Optional[str]:
        if not data:
            return None
            
        try:
            with get_db() as db:
                result = db.execute(
                    text("SELECT encode(pgp_sym_encrypt(:data, :password), 'base64') as encrypted_data"),
                    {"data": data, "password": password}
                ).fetchone()
                
                return result.encrypted_data if result else None
        except Exception as e:
            log.error(f"Encryption failed: {e}")
            return None
    
    def decrypt_data(encrypted_data: str, password: str) -> Optional[str]:
        if not encrypted_data:
            return None
            
        try:
            with get_db() as db:
                result = db.execute(
                    text("SELECT pgp_sym_decrypt(decode(:encrypted_data, 'base64'), :password) as decrypted_data"),
                    {"encrypted_data": encrypted_data, "password": password}
                ).fetchone()
                
                return result.decrypted_data if result else None
        except Exception as e:
            log.error(f"Decryption failed: {e}")
            return None
    
    def encrypt_vector(vector: List[float], encryption_key: str) -> Optional[str]:
        if not vector:
            return None
            
        try:
            vector_json = json.dumps(vector)
            return PgCrypto.encrypt_data(vector_json, encryption_key)
        except Exception as e:
            log.error(f"Vector encryption failed: {e}")
            return None
    
    def decrypt_vector(encrypted_vector: str, encryption_key: str) -> Optional[List[float]]:
        if not encrypted_vector:
            return None
            
        try:
            decrypted_json = PgCrypto.decrypt_data(encrypted_vector, encryption_key)
            if not decrypted_json:
                return None
            vector = json.loads(decrypted_json)
            
            if not isinstance(vector, list) or not all(isinstance(x, (int, float)) for x in vector):
                log.error("Decrypted vector data is not a valid list of numbers")
                return None
                
            return [float(x) for x in vector]
        except Exception as e:
            log.error(f"Vector decryption failed: {e}")
            return None


class EncryptionConfig:
    @classmethod
    def get_default_key(cls) -> str:
        return os.getenv("PGCRYPTO_DEFAULT_KEY", "fallback-default-key-change-in-production")
    
    @classmethod
    def validate_keys(cls) -> bool:
        keys = [
            ("PGCRYPTO_DEFAULT_KEY", cls.get_default_key())
        ]
        
        all_valid = True
        for key_name, key_value in keys:
            if not key_value or key_value.startswith("fallback-") or key_value.startswith("your-secure-"):
                log.warning(f"Encryption key {key_name} is not properly configured. Please set it in environment variables.")
                all_valid = False
                
        return all_valid
