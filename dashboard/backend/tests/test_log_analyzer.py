import os
import tempfile

import pytest
from app.log_analyzer import analyze_logs


@pytest.fixture
def sample_log_file():
    """Create a temporary Nginx-style log file for testing."""
    log_data = """127.0.0.1 - - [07/Nov/2025:12:00:00 +0000] "GET /index.html HTTP/1.1" 200
192.168.0.2 - - [07/Nov/2025:12:01:00 +0000] "POST /login HTTP/1.1" 403
127.0.0.1 - - [07/Nov/2025:12:02:00 +0000] "GET /about HTTP/1.1" 200
"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write(log_data)
        tmp_path = f.name
    yield tmp_path
    os.remove(tmp_path)


def test_analyze_logs_valid_file(sample_log_file):
    """Ensure log analyzer correctly counts requests, status codes, and IPs."""
    result = analyze_logs(sample_log_file)

    assert "total_requests" in result
    assert result["total_requests"] == 3
    assert result["unique_visitors"] == 2
    assert "200" in result["status_counts"]
    assert "top_ips" in result
    assert result["top_ips"][0][0] == "127.0.0.1"


def test_analyze_logs_missing_file():
    """Ensure analyzer gracefully handles missing file."""
    result = analyze_logs("non_existent.log")

    assert "error" in result
    assert "not found" in result["error"].lower()
