import socket

def grab_banner(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                data = sock.recv(1024)
                banner = data.decode().strip()
                return banner
            return None
    except (socket.timeout, TimeoutError, ConnectionRefusedError, OSError):
        return None