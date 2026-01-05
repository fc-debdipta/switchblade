import time
from src.utils.switchblade_decorator import tool


@tool(
    name="cve_check",
    description="Checks a specific service version against a local CVE database.",
    input_schema={
        "type": "object",
        "properties": {"service": {"type": "string"}, "version": {"type": "string"}},
        "required": ["service", "version"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "vulnerable": {"type": "boolean"},
            "cves": {"type": "array", "items": {"type": "string"}},
            "severity": {
                "type": "string",
                "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            },
        },
    },
)
def cve_check(args):
    service = args.get("service", "").lower()
    version = args.get("version", "")

    # Dummy logic: specific versions are "vulnerable"
    is_vuln = False
    cves = []
    severity = "LOW"

    if "nginx" in service and "1.18" in version:
        is_vuln = True
        cves = ["CVE-2021-23017"]
        severity = "HIGH"

    elif "mysql" in service and "5.7" in version:
        is_vuln = True
        cves = ["CVE-2020-14812", "CVE-2020-14765"]
        severity = "MEDIUM"

    elif "ssh" in service and "libssh" in version:
        is_vuln = True
        cves = ["CVE-2018-10933"]
        severity = "CRITICAL"

    return {
        "vulnerable": is_vuln,
        "cves": cves,
        "severity": severity if is_vuln else "NONE",
    }


@tool(
    name="check_sqli",
    description="Tests a URL parameter for SQL Injection vulnerabilities.",
    input_schema={
        "type": "object",
        "properties": {"url": {"type": "string"}, "param": {"type": "string"}},
        "required": ["url"],
    },
)
def check_sqli(args):
    url = args.get("url")
    param = args.get("param", "id")

    time.sleep(2)

    # Dummy logic: if param is "id", it's vulnerable
    if param == "id":
        return {
            "vulnerable": True,
            "payload_used": "' OR 1=1 --",
            "response_snippet": "SQL syntax error near '...'",
        }

    return {"vulnerable": False, "message": "Parameters appear sanitized."}


@tool(
    name="check_s1",
    description="Tests a URL parameter for SQL Injection vulnerabilities.",
    input_schema={
        "type": "object",
        "properties": {"url": {"type": "string"}, "param": {"type": "string"}},
        "required": ["url"],
    },
)
def check_s1(args):
    url = args.get("url")
    param = args.get("param", "id")

    time.sleep(2)

    # Dummy logic: if param is "id", it's vulnerable
    if param == "id":
        return {
            "vulnerable": True,
            "payload_used": "' OR 1=1 --",
            "response_snippet": "SQL syntax error near '...'",
        }

    return {"vulnerable": False, "message": "Parameters appear sanitized."}
