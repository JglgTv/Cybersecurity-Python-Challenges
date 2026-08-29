import sys
import urllib.request
from urllib.error import HTTPError, URLError
from typing import List

class DirectoryEnumerator:
    def __init__(self, target_url: str, wordlist_path: str):
        self.target_url = target_url if target_url.endswith('/') else target_url + '/'
        self.wordlist_path = wordlist_path
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def _load_wordlist(self) -> List[str]:
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            sys.exit(1)

    def enumerate(self) -> None:
        words = self._load_wordlist()
        
        for word in words:
            url = self.target_url + word
            req = urllib.request.Request(url, headers=self.headers, method='HEAD')
            
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(f"[{response.status}] {url}")
            except HTTPError as e:
                if e.code in [401, 403, 301, 302]:
                    print(f"[{e.code}] {url}")
            except URLError:
                continue
            except KeyboardInterrupt:
                sys.exit(0)

if __name__ == "__main__":
    target = ""
    wordlist = ""
    
    if len(sys.argv) == 3:
        target = sys.argv[1]
        wordlist = sys.argv[2]
    else:
        try:
            target = input("Enter target URL (e.g., http://example.com): ").strip()
            wordlist = input("Enter wordlist filepath: ").strip()
        except KeyboardInterrupt:
            sys.exit(1)
            
    if not target or not wordlist:
        sys.exit(1)
        
    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    enumerator = DirectoryEnumerator(target, wordlist)
    enumerator.enumerate()
