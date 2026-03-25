import json

def print_report(target, ip, port, open_ports, banners):
    print("=" * 40)
    print(f" netrecon - Scan Report")
    print("=" * 40)
    print(f" {'Target':<10} : {target}")
    print(f" {'IP':<10} : {ip}")
    print(f" {'Ports':<10} : {port}")
    print("=" * 40)
    print(f" {'PORT':<10} {'STATE':<10} {'BANNER'}")
    print("-" * 40)
    for port, banner in zip(open_ports, banners):
        banner_text = banner if banner else "N/A"
        print(f" {str(port):<10} {'open':<10} {banner_text}")
    print("=" * 40)

def save_report(target, ip, open_ports, banners, filename):
    report = {
        "target": target,
        "ip": ip,
        "open_ports": [
            {"port": port, "banner": banner if banner else "N/A"}
            for port, banner in zip(open_ports, banners)
        ]
    }
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
    print(f"[*] Report saved to {filename}")
