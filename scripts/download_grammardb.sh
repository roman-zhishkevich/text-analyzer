#!/bin/bash
# Download and extract GrammarDB from official GitHub releases

set -e

echo "📥 Downloading GrammarDB RELEASE-202601..."

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download latest release (RELEASE-202601)
echo "Downloading RELEASE-202601.zip..."
curl -L -o grammardb.zip \
  "https://github.com/Belarus/GrammarDB/releases/download/RELEASE-202601/RELEASE-202601.zip"

# Extract
echo "📂 Extracting..."
unzip -q grammardb.zip

# Show contents
echo "✅ Downloaded and extracted to: $TEMP_DIR"
echo ""
echo "📁 Contents:"
ls -lh

echo ""
echo "Next steps:"
echo "1. Review the XML files in: $TEMP_DIR"
echo "2. Run: python scripts/convert_grammardb_to_json.py $TEMP_DIR data/grammardb.json"
echo ""
echo "Temp directory: $TEMP_DIR"

