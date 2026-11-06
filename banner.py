import socket

HTTP_PORTS = {80, 8000, 8008, 8080, 8888}

def grab_banner(target, port, timeout=1.0, host=None):
    try:
        with socket.create_connection((target, port), timeout=timeout) as sock:
            sock.settimeout(timeout)

            if port in HTTP_PORTS:
                request = (
                    f"HEAD / HTTP/1.0\r\n"
                    f"Host: {host or target}\r\n"
                    f"Connection: close\r\n\r\n"
                )
                sock.sendall(request.encode())

            data = sock.recv(1024)

    except OSError:
        return None

    text = data.decode(errors="replace").strip()

    if not text:
        return None

    if port in HTTP_PORTS:
        for line in text.splitlines():
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()
    return text.splitlines()[0]
