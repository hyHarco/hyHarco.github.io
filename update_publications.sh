#!/bin/bash

echo "🐍 [STEP 0] Checking Python venv..."

if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q --disable-pip-version-check requests beautifulsoup4

echo "📚 [STEP 1] Running publication scraper..."
python3 scripts/scrape_scholar.py

if [ $? -ne 0 ]; then
    echo "❌ Scraper failed. Aborting."
    exit 1
fi

echo "✅ Scraping complete. Showing recent publications:"
jq '.[0:3]' publication/publications.json