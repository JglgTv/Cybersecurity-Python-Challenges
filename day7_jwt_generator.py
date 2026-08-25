import json
import base64
import hmac
import hashlib
import time
import sys
from typing import Dict, Any, Tuple

class JWTManager:
    def __init__(self, secret: str):
        if not secret:
            raise ValueError("Secret key cannot be empty.")
        self.secret = secret.encode('utf-8')

    @staticmethod
    def _base64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    @staticmethod
    def _base64url_decode(data: str) -> bytes:
        padding = '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data + padding)

    def generate(self, payload: Dict[str, Any]) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        
        b64_header = self._base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
        b64_payload = self._base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
        
        signature_input = f"{b64_header}.{b64_payload}".encode('utf-8')
        signature = hmac.new(self.secret, signature_input, hashlib.sha256).digest()
        b64_signature = self._base64url_encode(signature)
        
        return f"{b64_header}.{b64_payload}.{b64_signature}"

    def verify(self, token: str) -> Tuple[bool, Dict[str, Any]]:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return False, {}
                
            header_b64, payload_b64, signature_b64 = parts
            
            signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
            expected_signature = hmac.new(self.secret, signature_input, hashlib.sha256).digest()
            expected_signature_b64 = self._base64url_encode(expected_signature)
            
            if not hmac.compare_digest(signature_b64, expected_signature_b64):
                return False, {}
                
            payload = json.loads(self._base64url_decode(payload_b64).decode('utf-8'))
            
            if 'exp' in payload and payload['exp'] < int(time.time()):
                return False, {}
                
            return True, payload
        except Exception:
            return False, {}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "generate" and len(sys.argv) == 4:
            secret = sys.argv[2]
            user = sys.argv[3]
            manager = JWTManager(secret)
            payload = {
                "sub": user,
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600
            }
            print(manager.generate(payload))
            sys.exit(0)
        elif mode == "verify" and len(sys.argv) == 4:
            secret = sys.argv[2]
            token = sys.argv[3]
            manager = JWTManager(secret)
            is_valid, decoded_payload = manager.verify(token)
            if is_valid:
                print(f"Valid: {json.dumps(decoded_payload)}")
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            sys.exit(1)
    else:
        try:
            mode = input("Mode (generate/verify): ").strip().lower()
            secret = input("Secret key: ").strip()
            manager = JWTManager(secret)
            
            if mode == "generate":
                user = input("Subject (username): ").strip()
                payload = {
                    "sub": user,
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 3600
                }
                print(f"\nToken:\n{manager.generate(payload)}")
            elif mode == "verify":
                token = input("JWT Token: ").strip()
                is_valid, decoded_payload = manager.verify(token)
                if is_valid:
                    print(f"\nSignature Valid.\nPayload: {json.dumps(decoded_payload)}")
                else:
                    print("\nInvalid Token or Signature.")
            else:
                sys.exit(1)
        except (KeyboardInterrupt, ValueError):
            sys.exit(1)
