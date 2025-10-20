"""
src/utils/helpers.py
Utility functions for cleaning, normalizing, and deduplicating job data.
"""

import hashlib
import re
from datetime import datetime, timezone
from typing import List, Dict, Any
import os
import yaml

def normalize_text(text: str) -> str:
    """
    Cleans up whitespace and ensures text is consistent.

    Args:
        text: Input text string

    Returns:
        str: Normalized text with consistent whitespace
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def generate_job_id(source: str, url: str, title: str) -> str:
    """
    Generates a unique deterministic hash for a job using its source + url + title.

    Args:
        source: Job source (e.g., "remoteok", "remotive")
        url: Job URL
        title: Job title

    Returns:
        str: MD5 hash of the combined source:url:title
    """
    base_string = f"{source}:{url}:{title}"
    return hashlib.md5(base_string.encode("utf-8")).hexdigest()


def parse_date(date_str: str) -> str:
    """
    Tries to normalize different date formats into a consistent ISO8601 string.
    Returns today's date if parsing fails.

    Args:
        date_str: Date string in various formats

    Returns:
        str: ISO8601 formatted date string
    """
    if not date_str:
        return datetime.now(timezone.utc).isoformat()

    try:
        # Handle ISO or common formats
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).isoformat()
    except Exception:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").isoformat()
        except Exception:
            return datetime.now(timezone.utc).isoformat()


def deduplicate_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Removes duplicate job entries based on unique URL or title hash.
    Updates each job's "id" field with the generated hash.

    Args:
        jobs: List of job dictionaries

    Returns:
        List[Dict[str, Any]]: List of unique job dictionaries with updated ids
    """
    seen = set()
    unique_jobs = []

    for job in jobs:
        uid = generate_job_id(
            job.get("source", ""),
            job.get("url", ""),
            job.get("title", "")
        )
        if uid not in seen:
            seen.add(uid)
            job["id"] = uid
            unique_jobs.append(job)

    return unique_jobs


def load_config(config_path="config/config.yaml"):
    """
    Load and parse the YAML configuration file.

    Args:
        config_path (str): Path to the YAML config file.
    Returns:
        dict: Parsed configuration data.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# Optional helper for logging timestamps
def timestamp():
    """Return current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")