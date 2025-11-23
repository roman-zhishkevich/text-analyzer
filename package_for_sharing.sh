#!/bin/bash
# Package Text Analyzer for sharing with another user

echo "📦 Packaging Text Analyzer for sharing..."

cd "$(dirname "$0")"

# Create package name with date
DATE=$(date +%Y%m%d)
PACKAGE_NAME="text-analyzer-${DATE}.zip"

# Create zip excluding unnecessary files
zip -r "${PACKAGE_NAME}" . \
    -x "*.git*" \
    -x "*venv/*" \
    -x "*__pycache__/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*.DS_Store" \
    -x "*package_for_sharing.sh" \
    -x "*.egg-info/*" \
    -x ".alerus/*"

echo ""
echo "✅ Package created: ${PACKAGE_NAME}"
echo ""
echo "📤 To share with another person:"
echo "   1. Send them the file: ${PACKAGE_NAME}"
echo "   2. They should read: INSTALL_FOR_USER.md"
echo ""
echo "📋 File size:"
ls -lh "${PACKAGE_NAME}" | awk '{print "   " $5}'


