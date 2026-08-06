import socket
import sys
from typing import List, Dict

class PortScanner:
    def __init__(self, target: str, timeout: float = 1.0):
        self.target = target
        self.timeout = timeout
        try:
            self.target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            self.target_ip = None

    def get_ip(self) -> str:
        return self.target_ip if self.target_ip else "Invalid Host"

    def scan(self, ports: List[int]) -> Dict[int, str]:
        results = {}
        if not self.target_ip:
            return results

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # connect_ex returns 0 if the connection was successful
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:
                results[port] = "OPEN"
            else:
                results[port] = "CLOSED"
                
            sock.close()
            
        return results

if __name__ == "__main__":
    target_host = ""
    
    if len(sys.argv) > 1:
        target_host = sys.argv[1]
    else:
        try:
            target_host = input("Enter target IP or domain: ").strip()
        except KeyboardInterrupt:
            sys.exit(1)
            
    if not target_host:
        sys.exit(1)

    # Common ports: FTP(21), SSH(22), HTTP(80), HTTPS(443), RDP(3389)
    ports_to_scan = [21, 22, 80, 443, 3389]
    
    scanner = PortScanner(target_host)
    ip_address = scanner.get_ip()
    
    if ip_address == "Invalid Host":
        print(f"Error: Could not resolve host '{target_host}'.")
        sys.exit(1)
        
    print(f"\nScanning target: {target_host} ({ip_address})")
    print("-" * 35)
    
    scan_results = scanner.scan(ports_to_scan)
    
    for port, status in scan_results.items():
        print(f"Port {port:<5} : {status}")
