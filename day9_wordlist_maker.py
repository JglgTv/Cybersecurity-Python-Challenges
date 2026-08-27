import sys
import itertools
from typing import List

class WordlistGenerator:
    def __init__(self, charset: str, min_len: int, max_len: int):
        if min_len > max_len or min_len < 1:
            raise ValueError("Invalid length constraints.")
        if not charset:
            raise ValueError("Charset cannot be empty.")
        self.charset = charset
        self.min_len = min_len
        self.max_len = max_len

    def generate_to_file(self, output_filepath: str) -> int:
        count = 0
        try:
            with open(output_filepath, 'w', encoding='utf-8') as file:
                for length in range(self.min_len, self.max_len + 1):
                    for combination in itertools.product(self.charset, repeat=length):
                        file.write("".join(combination) + "\n")
                        count += 1
            return count
        except IOError:
            sys.exit(1)

if __name__ == "__main__":
    charset = ""
    min_len = 0
    max_len = 0
    output_file = ""

    if len(sys.argv) == 5:
        charset = sys.argv[1]
        try:
            min_len = int(sys.argv[2])
            max_len = int(sys.argv[3])
            output_file = sys.argv[4]
        except ValueError:
            sys.exit(1)
    else:
        try:
            charset = input("Enter character set (e.g., abc123): ").strip()
            min_len = int(input("Enter minimum length: ").strip())
            max_len = int(input("Enter maximum length: ").strip())
            output_file = input("Enter output filename (e.g., wordlist.txt): ").strip()
        except (KeyboardInterrupt, ValueError):
            sys.exit(1)

    if not charset or not output_file:
        sys.exit(1)

    generator = WordlistGenerator(charset, min_len, max_len)
    total_words = generator.generate_to_file(output_file)

    print(f"Generated {total_words} combinations.")
    print(f"Saved to {output_file}.")
