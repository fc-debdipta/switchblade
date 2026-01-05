import time
import random
from src.utils.switchblade_decorator import tool


@tool(
    name="nmap_scan",
    description="Performs a TCP SYN scan on a target IP to find open ports and services.",
    input_schema={
        "type": "object",
        "properties": {
            "target_ip": {"type": "string", "description": "The IPv4 address to scan"},
            "scan_type": {"type": "string", "enum": ["quick", "full", "stealth"]},
        },
        "required": ["target_ip"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "open_ports": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "port": {"type": "integer"},
                        "service": {"type": "string"},
                        "version": {"type": "string"},
                    },
                },
            },
        },
    },
)
def nmap_scan(args):
    target = args.get("target_ip")
    scan_type = args.get("scan_type", "quick")

    # Simulate processing time
    time.sleep(1.5)

    # Deterministic dummy logic:
    # If IP ends in .1, it's a router. If .5, it's a web server. Else, random.
    last_octet = int(target.split(".")[-1]) if "." in target else 0

    results = []

    if last_octet == 1:
        results = [
            {"port": 22, "service": "ssh", "version": "OpenSSH 8.2p1"},
            {"port": 53, "service": "domain", "version": "dnsmasq 2.80"},
            {"port": 80, "service": "http", "version": "uhttpd"},
        ]
    elif last_octet == 5 or last_octet == 100:
        results = [
            {"port": 80, "service": "http", "version": "nginx 1.18.0"},
            {"port": 443, "service": "https", "version": "nginx 1.18.0"},
            {"port": 3306, "service": "mysql", "version": "MySQL 5.7.33"},
        ]
    else:
        results = [{"port": 22, "service": "ssh", "version": "OpenSSH 9.0"}]

    return {"status": "up", "scan_type": scan_type, "open_ports": results}


@tool(
    name="subdomain_finder",
    description="Enumerates subdomains for a given domain name.",
    input_schema={
        "type": "object",
        "properties": {"domain": {"type": "string"}},
        "required": ["domain"],
    },
)
def subdomain_finder(args):
    domain = args.get("domain")
    time.sleep(1)

    return {
        "domain": domain,
        "subdomains": [
            f"www.{domain}",
            f"api.{domain}",
            f"dev.{domain}",
            f"mail.{domain}",
            f"vpn.{domain}",
        ],
    }
