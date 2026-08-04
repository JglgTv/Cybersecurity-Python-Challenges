import sys

class CaesarCipher:
    def __init__(self, shift: int):
        self.shift = shift % 26

    def encrypt(self, text: str) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + self.shift) % 26 + base))
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, text: str) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base - self.shift) % 26 + base))
            else:
                result.append(char)
        return "".join(result)

if __name__ == "__main__":
    mode = ""
    text = ""
    shift = 3

    if len(sys.argv) > 2:
        mode = sys.argv[1].lower()
        text = sys.argv[2]
        if len(sys.argv) > 3:
            try:
                shift = int(sys.argv[3])
            except ValueError:
                sys.exit(1)
    else:
        try:
            mode = input("Enter mode (encrypt/decrypt): ").strip().lower()
            if mode not in ['encrypt', 'decrypt']:
                sys.exit(1)
            text = input("Enter text: ").strip()
            shift_input = input("Enter shift key (integer): ").strip()
            shift = int(shift_input) if shift_input else 3
        except (KeyboardInterrupt, ValueError):
            sys.exit(1)

    cipher = CaesarCipher(shift)

    if mode == "encrypt":
        print(cipher.encrypt(text))
    elif mode == "decrypt":
        print(cipher.decrypt(text))
