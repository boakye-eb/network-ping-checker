"""
Network Ping Checker
--------------------
Pings three targets in the same order used in my IT Support Troubleshooting Guide
and prints a plain-English diagnosis of where a connection problem is.

    1. Your router          -> is the problem between this computer and the router?
    2. A public IP address  -> is the problem beyond the router (e.g. the ISP)?
    3. A website name       -> is the problem DNS (name lookup)?

Usage:
    python ping_checker.py                      # asks for your router IP
    python ping_checker.py --router 192.168.1.1
    python ping_checker.py --router 192.168.1.1 --log results.csv

Works on Windows, macOS and Linux. Uses only the Python standard library.
"""

import argparse
import csv
import platform
import re
import subprocess
from datetime import datetime

PUBLIC_IP = "8.8.8.8"        # Google's public DNS server, used to test the internet itself
WEBSITE = "google.com"       # Used to test DNS (turning a name into an IP address)


def ping(host):
    """Ping a host 4 times. Returns (is_up, average_ms or None)."""
    # Windows uses -n for the packet count; macOS/Linux use -c.
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", count_flag, "4", host],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, None

    if result.returncode != 0:
        return False, None

    # Pull each "time=24ms" (or "time<1ms") value out of the output and average them.
    times = [float(t) for t in re.findall(r"time[=<]\s*([\d.]+)", result.stdout)]
    if not times:
        return False, None
    return True, round(sum(times) / len(times))


def diagnose(router_up, ip_up, name_up):
    """Turn the three results into a plain-English conclusion."""
    if not router_up:
        return "Problem between this computer and the router. Check the cable or Wi-Fi, then restart the router."
    if not ip_up:
        return "Router is reachable but the internet is not. The problem is beyond the router (likely the ISP)."
    if not name_up:
        return "Internet works by IP address but not by name. This looks like a DNS problem."
    return "All three checks passed. The connection looks healthy."


def save_to_log(path, rows):
    """Append results to a CSV file so you can compare them over time."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["time", "check", "target", "status", "avg_ms"])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Ping your router, a public IP and a website, then diagnose.")
    parser.add_argument("--router", help="your router's IP address, e.g. 192.168.1.1")
    parser.add_argument("--log", help="optional CSV file to save the results to")
    args = parser.parse_args()

    router = args.router or input("Enter your router's IP address (e.g. 192.168.1.1): ").strip()

    checks = [
        ("Router", router),
        ("Public IP", PUBLIC_IP),
        ("Website (DNS)", WEBSITE),
    ]

    print("\nRunning checks...\n")
    statuses = []
    log_rows = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for label, target in checks:
        is_up, avg_ms = ping(target)
        statuses.append(is_up)
        status = "UP" if is_up else "DOWN"
        speed = f"{avg_ms} ms" if avg_ms is not None else "-"
        print(f"{label:<15} {target:<18} {status:<5} {speed}")
        log_rows.append([now, label, target, status, avg_ms if avg_ms is not None else ""])

    print("\nDiagnosis:", diagnose(*statuses))

    if args.log:
        save_to_log(args.log, log_rows)
        print(f"Results saved to {args.log}")


if __name__ == "__main__":
    main()
