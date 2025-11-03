import re
from collections import Counter

Log_file = "/data/data/com.termux/files/usr/var/log/nginx/access.log"

log_regex = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<time>.*?)\] '
    r'"(?P<method>\S+) (?P<request>\S+) (?P<proto>\S+)" '
    r'(?P<status>\d{3})'
)

def analyze_logs():
    try:
        with open(Log_file, 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        return {"error": f"Log file at {Log_file} not found."}
    
    total_requests = 0
    status_counts = Counter()
    ip_counts = Counter()
    endpoint_counts = Counter()

    for line in logs: 
        match = log_regex.search(line)
        if not match:
            continue

        total_requests += 1
        data = match.groupdict()

        status_counts[data['status']] += 1
        ip_counts[data['ip']] += 1
        endpoint_counts[data['request']] += 1

    # --- MOVED THIS BLOCK ---
    # These calculations must happen AFTER the loop is finished.
    top_ips = ip_counts.most_common(5)
    top_endpoints = endpoint_counts.most_common(5)
    top_status = status_counts.most_common(5)

    return {
        "total_requests": total_requests,
        "status_counts": dict(status_counts),
        "unique_visitors": len(ip_counts), # Added this, it's a useful metric
        "top_ips": top_ips,
        "top_endpoints": top_endpoints,
        "top_status": top_status
    }