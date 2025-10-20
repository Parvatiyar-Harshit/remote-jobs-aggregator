"""
src/main.py
Main orchestrator that fetches jobs from multiple sources,
applies filters and deduplication, and saves them to the SQLite DB.
"""

import sqlite3
from src.scraper.remoteok_scraper import fetch_remoteok_jobs
from src.scraper.remotive_scraper import fetch_remotive_jobs
from src.filters.usd_remote_filter import filter_jobs
from src.utils.helpers import normalize_text, deduplicate_jobs, generate_job_id, load_config
from src.db.models import init_db


def clean_job(job, source):
    """
    Normalize text fields and attach metadata.

    Args:
        job: Job dictionary from scraper
        source: Source identifier (e.g., "remoteok", "remotive")

    Returns:
        dict: Cleaned job with normalized fields and metadata
    """
    job["source"] = source
    job["title"] = normalize_text(job.get("title", ""))
    job["company"] = normalize_text(job.get("company", ""))
    job["url"] = job.get("url", "").strip()
    job["id"] = generate_job_id(source, job["url"], job["title"])
    return job


def save_jobs_to_db(conn, jobs):
    """
    Inserts jobs into SQLite DB while skipping duplicates.

    Args:
        conn: SQLite3 connection object
        jobs: List of job dictionaries to insert
    """
    cursor = conn.cursor()
    inserted = 0

    for job in jobs:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO jobs (id, title, company, location, salary, url, source, date_posted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.get("id"),
                    job.get("title"),
                    job.get("company"),
                    job.get("location"),
                    job.get("salary"),
                    job.get("url"),
                    job.get("source"),
                    job.get("date"),
                ),
            )
            inserted += cursor.rowcount
        except sqlite3.Error as e:
            print(f"❌ Error inserting job {job.get('title')}: {e}")

    conn.commit()
    print(f"✅ Inserted {inserted} new jobs into DB.")


def main():
    """
    Main pipeline orchestrator.

    Fetches jobs from multiple sources, cleans, filters, deduplicates,
    and saves them to the SQLite database.
    """
    print("🚀 Starting job aggregation run...")
    config = load_config()
    conn = init_db()

    # Fetch jobs from all sources
    print("📥 Fetching jobs from sources...")
    remoteok_jobs = fetch_remoteok_jobs()
    remotive_jobs = fetch_remotive_jobs()

    print(f"Fetched {len(remoteok_jobs)} from RemoteOK, {len(remotive_jobs)} from Remotive.")

    # Clean and combine jobs
    print("🧹 Cleaning jobs...")
    all_jobs = [clean_job(j, "remoteok") for j in remoteok_jobs] + \
               [clean_job(j, "remotive") for j in remotive_jobs]

    print(f"Total jobs after combining: {len(all_jobs)}")

    # Filter and deduplicate
    print("🔍 Filtering jobs (remote + not INR)...")
    filtered = filter_jobs(all_jobs)
    print(f"Jobs after filtering: {len(filtered)}")

    print("🔄 Deduplicating jobs...")
    unique_jobs = deduplicate_jobs(filtered)
    print(f"Jobs after deduplication: {len(unique_jobs)}")

    # Save to database
    print("💾 Saving jobs to database...")
    save_jobs_to_db(conn, unique_jobs)
    conn.close()

    print("🏁 Run completed successfully.")


if __name__ == "__main__":
    main()

