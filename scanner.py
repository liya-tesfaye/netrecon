import concurrent.futures
import time 
import socket

def scan_port(target, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            return port
        return None

def scan_ports(target, start, end, timeout):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(scan_port,target, port, timeout) for port in range(start,end + 1)]
    
    open_ports = []

    for f in concurrent.futures.as_completed(results):
        if f.result() is not None:
            open_ports.append(f.result())

    elapsed = round(time.time() - start_time, 2)
    print(f"[*] Scan completed in {elapsed}s")
    return sorted(open_ports)