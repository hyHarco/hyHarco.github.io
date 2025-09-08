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

# 🆕 브랜치 만들기
BRANCH_NAME="update_publications"
echo "🌿 Creating new branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# 커밋 및 푸시
git add publication/publications.json
git commit -m "Update publications.json ($(date '+%Y-%m-%d'))"
git push -u origin "$BRANCH_NAME"

echo "🚀 Pushed to branch $BRANCH_NAME"
echo "➡️ Go to GitHub and create a Pull Request to merge into main"