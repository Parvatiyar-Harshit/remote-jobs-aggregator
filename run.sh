#!/bin/bash
# Remote Jobs Aggregator - Run Script

echo "===================================="
echo "🚀 Starting Remote Jobs Aggregator..."
echo "===================================="

# Activate virtual environment
source .venv/bin/activate

# Run the main ingestion pipeline
python -m src.main

echo "------------------------------------"
echo "✅ Pipeline complete!"
echo "📁 Output saved to: data/jobs.db"
echo "===================================="