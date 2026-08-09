import sys
import re
from collections import Counter
from typing import Dict

class LogAnalyzer:
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.failed_pattern = re.compile(r"Failed password for .* from (\d{1,3}(?:\.\d{1,3}){3})")

    def analyze_file(self, filepath: str) -> Dict[str, int]:
        ip_counts = Counter()
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    match = self.failed_pattern.search(line)
                    if match:
                        ip_counts[match.group(1)] += 1
        except FileNotFoundError:
            sys.exit(1)
        
        return {ip: count for ip, count in ip_counts.items() if count >= self.threshold}

if __name__ == "__main__":
    log_file = ""
    threshold = 5

    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        if len(sys.argv) > 2:
            try:
                threshold = int(sys.argv[2])
            except ValueError:
                sys.exit(1)
    else:
        try:
            log_file = input("Enter log file path: ").strip()
            t_input = input("Enter attempt threshold: ").strip()
            if t_input:
                threshold = int(t_input)
        except (KeyboardInterrupt, ValueError):
            sys.exit(1)

    if not log_file:
        sys.exit(1)

    analyzer = LogAnalyzer(threshold)
    flagged_ips = analyzer.analyze_file(log_file)

    print(f"{'IP ADDRESS':<20} {'FAILED ATTEMPTS':<15}")
    print("-" * 35)
    
    for ip, count in sorted(flagged_ips.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip:<20} {count:<15}")
