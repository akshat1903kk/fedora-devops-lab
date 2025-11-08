#!/usr/bin/env python3
"""
log_analyzer.py
----------------
Cross-platform, memory-efficient Nginx-style access log analyzer.

Highlights:
- Stream-based parsing (O(1) memory)
- Compatible with Linux & Windows file paths
- Graceful fallback if the log file doesn't exist
- Provides status, endpoint, and IP frequency analysis

Author: Akshat Kushwaha
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Union

# Flexible regex — supports IPv4/IPv6 and common Nginx log formats
LOG_PATTERN = re.compile(
    r"(?P<ip>[0-9a-fA-F\.:]+) - - \[(?P<time>[^\]]+)\] "
    r'"(?P<method>[A-Z]+) (?P<request>[^"]*?) (?P<proto>HTTP/[\d.]+)" '
    r"(?P<status>\d{3})"
)

# Default fallback path (Windows-safe)
DEFAULT_LOG_PATH = Path("app/test_logs/access.log")


# def analyze_logs(log_path: Union[str, Path]) -> dict:
#     """Analyze Nginx-style access logs and return summarized statistics."""

#     log_path = Path(log_path).expanduser().resolve()

#     if not log_path.exists():
#         # Fallback to a sample log (for local dev/testing)
#         if DEFAULT_LOG_PATH.exists():
#             log_path = DEFAULT_LOG_PATH
#         else:
#             return {"error": f"Log file not found: {log_path}"}

#     total_requests = 0
#     status_counts = Counter()
#     ip_counts = Counter()
#     endpoint_counts = Counter()

#     try:
#         # Use chunked streaming for big logs
#         with log_path.open("r", encoding="utf-8", errors="ignore") as f:
#             for line in f:
#                 # Skip empty or broken lines quickly
#                 if not line or '"' not in line:
#                     continue

#                 match = LOG_PATTERN.search(line)
#                 if not match:
#                     continue

#                 total_requests += 1
#                 entry = match.groupdict()

#                 status_counts[entry["status"]] += 1
#                 ip_counts[entry["ip"]] += 1
#                 endpoint_counts[entry["request"]] += 1

#     except (OSError, UnicodeDecodeError) as e:
#         return {"error": f"Failed to read log file: {e}"}


#     # Summarize results (no excessive JSON payloads)
#     return {
#         "log_file": str(log_path),
#         "total_requests": total_requests,
#         "unique_visitors": len(ip_counts),
#         "status_counts": dict(status_counts),
#         "top_ips": ip_counts.most_common(5),
#         "top_endpoints": endpoint_counts.most_common(5),
#         "top_status_codes": status_counts.most_common(5),
#         "error_summary": {
#             code: count
#             for code, count in status_counts.items()
#             if code.startswith(("4", "5"))
#         },
#     }
#
def analyze_logs(log_path: str | Path) -> dict:
    """Analyze an Nginx access log file and return aggregated stats."""

    log_path = Path(log_path)
    if not log_path.exists():
        return {"error": f"Log file not found: {log_path}"}

    total_requests = 0
    status_counts = Counter()
    ip_counts = Counter()
    endpoint_counts = Counter()

    try:
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
    except Exception as e:
        return {"error": f"Failed to read log file: {e}"}

    # Always return a consistent structure
    return {
        "log_file": str(log_path),
        "total_requests": total_requests,
        "unique_visitors": len(ip_counts),
        "status_counts": dict(status_counts),
        "top_ips": ip_counts.most_common(5),
        "top_endpoints": endpoint_counts.most_common(5),
        "error_summary": {
            code: count
            for code, count in status_counts.items()
            if code.startswith(("4", "5"))
        },
    }


def main():
    """CLI entrypoint — can be used independently on Windows or Linux."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze Nginx-style access logs and output JSON stats."
    )
    parser.add_argument(
        "logfile",
        nargs="?",
        default=str(DEFAULT_LOG_PATH),
        help="Path to log file (defaults to app/test_logs/access.log if missing).",
    )
    args = parser.parse_args()

    result = analyze_logs(args.logfile)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
