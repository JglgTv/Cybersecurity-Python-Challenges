import sys
import urllib.request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from typing import Dict, List, Tuple

class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags: List[Dict[str, str]] = []
        self.comments: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]):
        if tag == "meta":
            self.meta_tags.append(dict(attrs))

    def handle_comment(self, data: str):
        cleaned_comment = data.strip()
        if cleaned_comment:
            self.comments.append(cleaned_comment)

class MetadataScraper:
    def __init__(self, target_url: str):
        if not target_url.startswith(("http://", "https://")):
            self.target_url = "http://" + target_url
        else:
            self.target_url = target_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def scrape(self) -> None:
        try:
            req = urllib.request.Request(self.target_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                http_headers = response.getheaders()
                html_content = response.read().decode('utf-8', errors='ignore')

            print(f"\n[+] Target: {self.target_url}")
            print("\n--- HTTP Headers (Server Info) ---")
            for key, value in http_headers:
                print(f"{key}: {value}")

            parser = MetadataParser()
            parser.feed(html_content)

            print("\n--- HTML Meta Tags ---")
            for meta in parser.meta_tags:
                print(meta)

            print("\n--- Hidden HTML Comments ---")
            for comment in parser.comments:
                print(f"<!-- {comment} -->")

        except HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            sys.exit(1)
        except URLError as e:
            print(f"URL Error: Failed to reach server. Reason: {e.reason}")
            sys.exit(1)
        except Exception as e:
            sys.exit(1)

if __name__ == "__main__":
    url = ""
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        try:
            url = input("Enter target URL (e.g., https://example.com): ").strip()
        except KeyboardInterrupt:
            sys.exit(1)
            
    if not url:
        sys.exit(1)

    scraper = MetadataScraper(url)
    scraper.scrape()
