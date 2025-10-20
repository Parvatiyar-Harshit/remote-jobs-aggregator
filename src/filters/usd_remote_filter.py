import re
from typing import List, Dict, Any
from src.utils.helpers import load_config


def is_remote(job: Dict[str, Any]) -> bool:
    """
    Check if a job is remote based on location, title, and tags.

    Args:
        job: Job dictionary

    Returns:
        bool: True if job is remote, False otherwise
    """
    remote_keywords = ["remote", "anywhere", "global", "worldwide", "distributed"]

    # Combine location, title, and tags into a single searchable string
    searchable_text = " ".join([
        job.get("location", ""),
        job.get("title", ""),
        job.get("tags", "")
    ]).lower()

    # Check if any remote keyword appears in the searchable text
    for keyword in remote_keywords:
        if re.search(r"\b" + keyword + r"\b", searchable_text):
            return True

    return False


def is_not_inr(job: Dict[str, Any]) -> bool:
    """
    Check if a job does NOT pay in excluded currencies (from config).

    Args:
        job: Job dictionary

    Returns:
        bool: True if job is NOT in excluded currencies, False otherwise
    """
    config = load_config()
    excluded_currencies = config["filter"]["exclude_currencies"]

    # Combine salary and other relevant fields
    searchable_text = " ".join([
        str(job.get("salary", "")),
        job.get("title", ""),
        job.get("tags", "")
    ])

    # Check if any excluded currency appears
    for currency in excluded_currencies:
        if currency in searchable_text:
            return False

    return True


def filter_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter jobs to keep only remote/global jobs that are not INR-based and remove duplicates.

    Args:
        jobs: List of job dictionaries

    Returns:
        List[Dict[str, Any]]: Filtered list of jobs
    """
    seen_ids = set()
    filtered_jobs = []

    for job in jobs:
        # Skip if we've already seen this job ID
        job_id = job.get("id", "")
        if job_id in seen_ids:
            continue

        # Check if job is remote and not INR-based
        if is_remote(job) and is_not_inr(job):
            seen_ids.add(job_id)
            filtered_jobs.append(job)

    return filtered_jobs


if __name__ == "__main__":
    from src.scraper.remoteok_scraper import fetch_remoteok_jobs

    jobs = fetch_remoteok_jobs()
    filtered = filter_jobs(jobs)
    print(f"Filtered {len(filtered)} out of {len(jobs)} jobs.")
    if len(filtered) > 0:
        print("\nFirst filtered job:")
        print(filtered[0])
    if len(filtered) > 1:
        print("\nSecond filtered job:")
        print(filtered[1])

