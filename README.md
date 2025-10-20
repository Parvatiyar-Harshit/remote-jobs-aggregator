# 🧠 Remote Jobs Aggregator (USD-paying / Remote-friendly)

This project is a **lightweight job aggregator** that fetches remote job listings from public APIs (currently **RemoteOK** and **Remotive.io**) and stores the results in a local **SQLite** database after filtering out non-remote or INR-paying jobs.

It’s designed for:
- Developers in India/SEA seeking **USD-paying** remote roles
- A **free-tier, low-maintenance** setup
- Future automation via AWS and simple bot integrations (Telegram or Web)

---

## 🚀 Features

- Fetches jobs from **RemoteOK** and **Remotive.io**
- Filters jobs for **remote availability** and excludes **INR** listings
- Deduplicates entries before saving
- Stores filtered jobs in **SQLite**
- Fully **local**, no paid dependencies or hosting needed

---

## 🧰 Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Parvatiyar-Harshit/remote-jobs-aggregator.git
cd remote-jobs-aggregator
2. Create and Activate a Virtual Environment
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Run the Pipeline
This command will fetch jobs from both sources, apply filters, and save results in data/jobs.db.

bash
Copy code
bash run.sh
Output will include the total jobs fetched, filtered, and stored.

📁 Project Structure
bash
Copy code
remote-jobs-aggregator/
│
├── config/
│   └── config.yaml              # Global config (paths, URLs, settings)
│
├── data/                        # Stores SQLite DB and temporary files
│
├── src/
│   ├── db/                      # Database schema and models
│   ├── scraper/                 # Scrapers for APIs
│   ├── filters/                 # Filtering logic for relevant jobs
│   ├── utils/                   # Helper functions
│   ├── notifier/                # Placeholder for future notification system
│   └── main.py                  # Orchestration script
│
├── tests/                       # Basic test suite
│
├── requirements.txt             # Dependencies
├── run.sh                       # Run pipeline script
├── .gitignore                   # Ignore unwanted files
└── README.md                    # Project documentation
🧩 Tech Stack
Language: Python 3.10+

Database: SQLite (local, lightweight)

APIs: RemoteOK, Remotive.io

Hosting: (Planned) AWS Free Tier

Automation: (Planned) cron/AWS Lambda

🪴 Next Steps
 Add a Telegram notifier or Google Sheets output

 Deploy as a daily automation on AWS

 Expand data sources

 Build a simple web frontend

 Add analytics or monetization hooks

👨‍💻 Author: Parvatiyar-Harshit
🕒 Status: Phase 1 Complete — Data ingestion layer working
