import os
import tempfile

import pytest
from app.log_analyzer import analyze_logs


@pytest.fixture
def sample_log_file():
    log_data = """127.0.0.1 - - [07/Nov/2025:12:00:00 +0000] "GET /index.html HTTP/1.1" 200
192.168.0.2 - - [07/Nov/2025:12:01:00 +0000] "POST /login HTTP/1.1" 403
127.0.0.1 - - [07/Nov/2025:12:02:00 +0000] "GET /about HTTP/1.1" 200
"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
        f.write(log_data)
        tmp_path = f.name
    yield tmp_path
    os.remove(tmp_path)


def test_analyze_logs_valid_file(sample_log_file):
    """Validate analyzer output structure and accuracy."""
    result = analyze_logs(sample_log_file)
    assert isinstance(result, dict)
    assert result.get("total_requests", 0) == 3
    assert result.get("unique_visitors", 0) == 2
    assert "200" in result.get("status_counts", {})


def test_analyze_logs_missing_file():
    """Ensure missing log returns structured error response."""
    result = analyze_logs("non_existent.log")
    assert isinstance(result, dict)
    assert "error" in result
    assert "not found" in result["error"].lower()
