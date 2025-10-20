from src.utils.helpers import (
    normalize_text,
    generate_job_id,
    parse_date,
    deduplicate_jobs,
    load_config,
    timestamp,
)
from datetime import datetime


def test_normalize_text():
    assert normalize_text("   Hello   World  ") == "Hello World"
    assert normalize_text("\nJob\tTitle ") == "Job Title"
    print("✅ normalize_text works")


def test_generate_job_id():
    id1 = generate_job_id("remoteok", "https://example.com/job/1", "Dev")
    id2 = generate_job_id("remoteok", "https://example.com/job/1", "Dev")
    assert id1 == id2  # Deterministic
    id3 = generate_job_id("remoteok", "https://example.com/job/2", "Dev")
    assert id1 != id3  # Unique
    print("✅ generate_job_id works")


def test_parse_date():
    d1 = parse_date("2024-10-01")
    d2 = parse_date(None)
    assert isinstance(d1, str) and len(d1) > 0
    assert isinstance(d2, str)
    print("✅ parse_date works")


def test_deduplicate_jobs():
    jobs = [
        {"source": "remoteok", "url": "https://a.com", "title": "Engineer"},
        {"source": "remoteok", "url": "https://a.com", "title": "Engineer"},
        {"source": "remotive", "url": "https://b.com", "title": "Designer"},
    ]
    deduped = deduplicate_jobs(jobs)
    assert len(deduped) == 2
    print("✅ deduplicate_jobs works")


def test_load_config():
    cfg = load_config("config/config.yaml")
    assert "scraper" in cfg
    assert isinstance(cfg["scraper"]["sources"], list)
    print("✅ load_config works")


def test_timestamp_format():
    ts = timestamp()
    assert len(ts) == 19  # "YYYY-MM-DD HH:MM:SS"
    assert ts[4] == "-" and ts[7] == "-" and ts[13] == ":"
    print("✅ timestamp_format works")


if __name__ == "__main__":
    print("\nRunning helper tests...\n")
    test_normalize_text()
    test_generate_job_id()
    test_parse_date()
    test_deduplicate_jobs()
    test_load_config()
    test_timestamp_format()
    print("\n🎉 All helper tests passed!")
