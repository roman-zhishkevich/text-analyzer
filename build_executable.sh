#!/bin/bash
# Build standalone executable for Text Analyzer

echo "🔨 Building Text Analyzer Desktop Executable"
echo ""

# Check if in correct directory
if [ ! -f "TextAnalyzer.spec" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Activating venv..."
    source venv/bin/activate || {
        echo "❌ Failed to activate venv. Please run:"
        echo "   source venv/bin/activate"
        exit 1
    }
fi

# Install PyInstaller if not present
echo "📦 Checking PyInstaller..."
pip show pyinstaller > /dev/null 2>&1 || {
    echo "   Installing PyInstaller..."
    pip install pyinstaller
}

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.spec~ 

# Build executable
echo "🔨 Building executable (this takes 5-10 minutes)..."
echo ""
pyinstaller TextAnalyzer.spec

# Check if build succeeded
if [ -f "dist/TextAnalyzer" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📍 Executable location: dist/TextAnalyzer"
    echo "📊 File size:"
    ls -lh dist/TextAnalyzer | awk '{print "   " $5}'
    echo ""
    echo "🧪 Test it:"
    echo "   ./dist/TextAnalyzer"
    echo ""
    echo "📦 To distribute:"
    echo "   zip -r TextAnalyzer.zip dist/TextAnalyzer"
    echo ""
else
    echo "❌ Build failed!"
    echo "   Check the error messages above"
    exit 1
fi


