import string
import secrets
import re
import sys

class PasswordManager:
    def __init__(self, length: int = 16):
        if length < 12:
            raise ValueError("Length must be at least 12 characters.")
        self.length = length
        self.characters = string.ascii_letters + string.digits + string.punctuation

    def generate_secure_password(self) -> str:
        while True:
            password = ''.join(secrets.choice(self.characters) for _ in range(self.length))
            if self.is_strong(password):
                return password

    @staticmethod
    def is_strong(password: str) -> bool:
        if len(password) < 12:
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not any(char in string.punctuation for char in password):
            return False
        return True

if __name__ == "__main__":
    manager = PasswordManager(length=16)
    
    if len(sys.argv) == 1:
        print(manager.generate_secure_password())
        sys.exit(0)
        
    if sys.argv[1] == "--generate":
        print(manager.generate_secure_password())
        sys.exit(0)
        
    if sys.argv[1] == "--validate" and len(sys.argv) > 2:
        is_valid = manager.is_strong(sys.argv[2])
        print(is_valid)
        sys.exit(0)
