import requests
from datetime import datetime
from typing import List, Dict, Any
from src.utils.helpers import load_config


def fetch_remotive_jobs() -> List[Dict[str, Any]]:
    """
    Fetch remote jobs from the Remotive.io API.

    Returns:
        List[Dict[str, Any]]: A list of job dictionaries with normalized data.
                              Returns empty list if fetch fails.
    """
    jobs = []

    try:
        config = load_config()
        api_url = config["scraper"]["sources"][1]["api_url"]
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract jobs from the top-level "jobs" key
        jobs_list = data.get("jobs", [])

        for job_data in jobs_list:
            try:
                # Extract tags as comma-separated string
                tags = job_data.get("tags", [])
                if isinstance(tags, list):
                    tags_str = ", ".join(tags)
                else:
                    tags_str = str(tags)

                # Parse publication_date to ISO format if possible
                date_str = job_data.get("publication_date", "")
                try:
                    # Try to parse the date and convert to ISO format
                    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    iso_date = date_obj.isoformat()
                except (ValueError, AttributeError):
                    # If parsing fails, use the original date string
                    iso_date = date_str

                # Extract salary, default to None if not available
                salary = job_data.get("salary", None)

                job = {
                    "id": f"remotive_{job_data.get('id', '')}",
                    "date": iso_date,
                    "title": job_data.get("title", ""),
                    "company": job_data.get("company_name", ""),
                    "location": job_data.get("candidate_required_location", ""),
                    "tags": tags_str,
                    "url": job_data.get("url", ""),
                    "salary": salary,
                    "source": "remotive"
                }

                jobs.append(job)
            except Exception as e:
                # Skip individual jobs that fail to parse
                print(f"Warning: Failed to parse job: {e}")
                continue

        return jobs

    except requests.exceptions.Timeout:
        print("Error: Request to Remotive API timed out")
        return []
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to Remotive API")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed: {e}")
        return []
    except ValueError as e:
        print(f"Error: Failed to parse JSON response: {e}")
        return []
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}")
        return []


if __name__ == "__main__":
    jobs = fetch_remotive_jobs()
    print(f"Total jobs fetched: {len(jobs)}")

    if len(jobs) > 0:
        print("\nFirst job:")
        print(jobs[0])

    if len(jobs) > 1:
        print("\nSecond job:")
        print(jobs[1])

