from utils import resolve_target, parse_ports, validate_timeout
from scanner import scan_ports
from banner import grab_banner
from reporter import print_report, save_report
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        prog='netrecon',
        description="Network reconnaissance tool for port scanning and banner grabbing.",
        epilog="Example: python main.py --target scanme.nmap.org --ports 1-1000"
    )
    parser.add_argument("-t", "--target", required=True, type=str, help='Enter the domain name or IP address of the target.')
    parser.add_argument("-p", "--ports", default="1-1000", type=str, help='Enter the start and end port range. Default 1-1000.')
    parser.add_argument("-o", "--output", type=str, help='Enter a file name.')
    parser.add_argument("--timeout", default=1.0, type=float, help='Connection timeout per port in seconds. Default: 1.0.')
    return parser.parse_args()

def main():
    args = parse_args()

    ip = resolve_target(args.target)
    print(f"[*] Resolved {args.target} → {ip}")

    start, end = parse_ports(args.ports)

    if not validate_timeout(args.timeout):
        print("[!] Timeout must be a positive number.")
        sys.exit(1)

    print(f"[*] Scanning ports {start}-{end} on {ip}...")
    open_ports = scan_ports(ip, start, end, args.timeout)

    if not open_ports:
        print("[!] No open ports found.")
        return

    print(f"[*] Grabbing banners...")
    banners = []
    for o_port in open_ports:
        banners.append(grab_banner(ip, o_port, args.timeout))

    print_report(args.target, ip, args.ports, open_ports, banners)

    if args.output:
        save_report(args.target, ip, open_ports, banners, args.output)

if __name__ == "__main__":
    main()