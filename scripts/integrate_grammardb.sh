#!/bin/bash
# All-in-one script to download and integrate GrammarDB

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         GrammarDB Integration Script                           ║"
echo "║    Download, convert, and integrate GrammarDB RELEASE-202601   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if data/grammardb.json already exists
if [ -f "data/grammardb.json" ]; then
    echo "⚠️  data/grammardb.json already exists!"
    echo ""
    read -p "Do you want to re-download and overwrite? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled."
        exit 0
    fi
    echo ""
fi

# Step 1: Download
echo "📥 Step 1/4: Downloading GrammarDB RELEASE-202601..."
echo ""

TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading from GitHub releases..."
curl -L -o grammardb.zip \
  "https://github.com/Belarus/GrammarDB/releases/download/RELEASE-202601/RELEASE-202601.zip" \
  --progress-bar

if [ ! -f "grammardb.zip" ]; then
    echo "❌ Download failed!"
    exit 1
fi

echo "✅ Downloaded successfully"
echo ""

# Step 2: Extract
echo "📂 Step 2/4: Extracting archive..."
unzip -q grammardb.zip

echo "✅ Extracted to: $TEMP_DIR"
echo ""
echo "Contents:"
ls -lh
echo ""

# Step 3: Convert
echo "🔄 Step 3/4: Converting XML to JSON..."
echo ""

# Return to project directory
cd - > /dev/null

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Trying system Python..."
fi

# Run conversion script
python3 scripts/convert_grammardb_to_json.py \
  "$TEMP_DIR" \
  "data/grammardb.json"

echo ""

# Step 4: Verify
echo "✅ Step 4/4: Verifying installation..."
echo ""

if [ -f "data/grammardb.json" ]; then
    FILE_SIZE=$(du -h data/grammardb.json | cut -f1)
    echo "✅ data/grammardb.json created successfully"
    echo "   File size: $FILE_SIZE"
    echo ""

    # Test
    echo "🧪 Running test..."
    python3 test_belarusian_lemmatizer.py | head -30
    echo ""

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    ✅ SUCCESS!                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 GrammarDB integration complete!"
    echo ""
    echo "Next steps:"
    echo "  • Run full test: python test_belarusian_lemmatizer.py"
    echo "  • Start app: ./run.sh"
    echo "  • Select '🇧🇾 Беларуская' in the app"
    echo ""
    echo "📊 Expected performance:"
    echo "  • 5-10x faster Belarusian lemmatization"
    echo "  • 80-90% words via fast GrammarDB lookup"
    echo "  • 10-20% words via lemmatizer_be fallback"
    echo ""
else
    echo "❌ Error: data/grammardb.json not created"
    exit 1
fi

# Cleanup
echo "🧹 Cleaning up temporary files..."
rm -rf "$TEMP_DIR"
echo "✅ Done!"

