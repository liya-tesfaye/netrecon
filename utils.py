import socket
import ipaddress
import sys

def is_valid_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

def resolve_target(target):
    if is_valid_ip(target):
        return target
    else:
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            print("[!] Could not resolve hostname.")
            sys.exit(1)

def parse_ports(port_string):
    parts = port_string.split("-")
    if len(parts) != 2:
        print("[!] Invalid port range format.")
        sys.exit(1)
    try:
        start = int(parts[0])
        end = int(parts[1])
    except ValueError:
        print("[!] Port values must be integers.")
        sys.exit(1)
    if start < 1 or end > 65535:
        print("[!] Invalid port range.")
        sys.exit(1)
    return(start,end)


def validate_timeout(timeout):
    if timeout > 0:
        return True
    else:
        return False