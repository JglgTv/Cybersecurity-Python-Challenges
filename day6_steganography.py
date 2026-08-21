import sys

class Steganography:
    DELIMITER = b"---SEC---"

    @staticmethod
    def hide(cover_filepath: str, secret_msg: str, output_filepath: str) -> bool:
        try:
            with open(cover_filepath, 'rb') as f:
                cover_data = f.read()
            
            payload = cover_data + Steganography.DELIMITER + secret_msg.encode('utf-8')
            
            with open(output_filepath, 'wb') as f:
                f.write(payload)
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def extract(stego_filepath: str) -> str:
        try:
            with open(stego_filepath, 'rb') as f:
                content = f.read()
            
            parts = content.split(Steganography.DELIMITER)
            if len(parts) > 1:
                return parts[-1].decode('utf-8')
            return ""
        except FileNotFoundError:
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "hide" and len(sys.argv) == 5:
            success = Steganography.hide(sys.argv[2], sys.argv[3], sys.argv[4])
            sys.exit(0 if success else 1)
        elif mode == "extract" and len(sys.argv) == 3:
            print(Steganography.extract(sys.argv[2]))
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        try:
            mode = input("Mode (hide/extract): ").strip().lower()
            if mode == "hide":
                cover = input("Cover file path: ").strip()
                msg = input("Secret message: ").strip()
                output = input("Output file path: ").strip()
                if Steganography.hide(cover, msg, output):
                    print("Data hidden successfully.")
                else:
                    sys.exit(1)
            elif mode == "extract":
                stego = input("Stego file path: ").strip()
                result = Steganography.extract(stego)
                if result:
                    print(f"Extracted: {result}")
            else:
                sys.exit(1)
        except (KeyboardInterrupt, ValueError):
            sys.exit(1)
