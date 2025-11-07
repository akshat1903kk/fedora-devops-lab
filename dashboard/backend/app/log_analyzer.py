#!/usr/bin/env python3
"""
log_analyzer.py
----------------
A lightweight, cross-platform Nginx access log analyzer.

Features:
- Stream-based parsing (no full file load into memory)
- Aggregates status codes, endpoints, and visitor IPs
- Returns both raw stats and top entries
- CLI-friendly JSON output for easy integration

Author: Akshat Kushwaha
"""

import json
import re
from collections import Counter
from pathlib import Path

# Regex pattern for standard Nginx access logs
LOG_PATTERN = re.compile(
    r"(?P<ip>[\d\.]+) - - \[(?P<time>[^\]]+)\] "
    r'"(?P<method>\S+) (?P<request>\S+) (?P<proto>\S+)" '
    r"(?P<status>\d{3})"
)


def analyze_logs(log_path: str | Path) -> dict:
    """Analyze an Nginx access log file and return aggregated stats."""

    log_path = Path(log_path)
    if not log_path.exists():
        return {"error": f"Log file not found: {log_path}"}

    total_requests = 0
    status_counts = Counter()
    ip_counts = Counter()
    endpoint_counts = Counter()

    # Stream file line-by-line to handle large logs efficiently
    with log_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if not match:
                continue

            total_requests += 1
            entry = match.groupdict()

            status_counts[entry["status"]] += 1
            ip_counts[entry["ip"]] += 1
            endpoint_counts[entry["request"]] += 1

    # Compute top results
    return {
        "total_requests": total_requests,
        "unique_visitors": len(ip_counts),
        "status_counts": dict(status_counts),
        "top_ips": ip_counts.most_common(5),
        "top_endpoints": endpoint_counts.most_common(5),
        "top_status_codes": status_counts.most_common(5),
        "error_summary": {
            code: count
            for code, count in status_counts.items()
            if code.startswith(("4", "5"))
        },
    }


def main():
    """CLI entrypoint."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze Nginx access logs and return summary stats."
    )
    parser.add_argument(
        "logfile",
        help="Path to the Nginx access log file (e.g. /var/log/nginx/access.log)",
    )
    args = parser.parse_args()

    result = analyze_logs(args.logfile)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
