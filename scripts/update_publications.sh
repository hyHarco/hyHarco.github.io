#!/bin/bash
set -e

echo "🐍 [STEP 0] Checking Python venv..."

if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

dependencies=(requests pyyaml)
if [[ " $* " != *" --no-enrich "* ]]; then
    dependencies+=(manubot)
fi

pip install -q --disable-pip-version-check "${dependencies[@]}"

echo "📚 [STEP 1] Updating publication data..."
if ! python3 scripts/update_publications.py "$@"; then
    echo "❌ Publication update failed. Aborting."
    exit 1
fi

echo "✅ Publication update complete."
