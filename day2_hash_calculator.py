import hashlib
import sys
from typing import Dict

class HashCalculator:
    def __init__(self, data: str):
        if not data:
            raise ValueError("Data cannot be empty.")
        self.data = data.encode('utf-8')
        
    def get_md5(self) -> str:
        return hashlib.md5(self.data).hexdigest()
        
    def get_sha1(self) -> str:
        return hashlib.sha1(self.data).hexdigest()
        
    def get_sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()
        
    def generate_report(self) -> Dict[str, str]:
        return {
            "MD5": self.get_md5(),
            "SHA-1": self.get_sha1(),
            "SHA-256": self.get_sha256()
        }

if __name__ == "__main__":
    input_data = ""
    
    if len(sys.argv) > 1:
        input_data = sys.argv[1]
    else:
        try:
            input_data = input("Enter text to hash: ").strip()
        except KeyboardInterrupt:
            sys.exit(1)
            
    if not input_data:
        sys.exit(1)
        
    calculator = HashCalculator(input_data)
    report = calculator.generate_report()
    
    for algorithm, hash_value in report.items():
        print(f"{algorithm:<10}: {hash_value}")
