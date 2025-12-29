from cryptography.fernet import Fernet
import os
from sqlalchemy.orm import Session
from app.models import AppSetting
from google import genai
import logging

# Ensure we have a key for encryption
KEY_FILE = "secret.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

cipher_suite = Fernet(load_or_create_key())

class KeyManager:
    def __init__(self, db: Session):
        self.db = db

    def save_key(self, provider: str, raw_key: str):
        """Encrypts and saves the API key. Validates it first."""
        # Validate
        if not self._validate_key(provider, raw_key):
             raise ValueError("Invalid API Key. Authentication failed.")

        encrypted_key = cipher_suite.encrypt(raw_key.encode())
        
        setting = self.db.query(AppSetting).filter(AppSetting.key == f"{provider}_api_key").first()
        if setting:
            setting.value = encrypted_key.decode()
        else:
            setting = AppSetting(key=f"{provider}_api_key", value=encrypted_key.decode())
            self.db.add(setting)
        
        self.db.commit()

    def get_decrypted_key(self, provider: str) -> str:
        setting = self.db.query(AppSetting).filter(AppSetting.key == f"{provider}_api_key").first()
        if not setting:
            return None
        try:
            return cipher_suite.decrypt(setting.value.encode()).decode()
        except:
            return None

    def _validate_key(self, provider: str, key: str) -> bool:
        if provider == "gemini":
            try:
                client = genai.Client(api_key=key)
                client.models.generate_content(
                    model="gemini-2.5-flash", contents="Test"
                )
                return True
            except Exception as e:
                logging.error(f"Key validation failed: {e}")
                return False
        return False
