#!/bin/bash
#
# Build script for Netlify deployment
# This script installs dependencies and builds the complete Skupper website
# including both Transom (main site + V1) and MkDocs (V2 docs with sidebar)
#

set -e  # Exit on error

echo "========================================="
echo "Skupper Website Build Script"
echo "========================================="

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install pyyaml mkdocs-material

# Verify installations
echo ""
echo "Verifying installations..."
python --version
pip list | grep -E "(pyyaml|mkdocs-material)"

# Build the complete site
echo ""
echo "Building complete site..."
echo "  Step 1: Transom (main site + V1 docs)"
echo "  Step 2: MkDocs (V2 docs with sidebar)"
./plano render

# Verify output
echo ""
echo "Verifying build output..."
if [ -d "output" ]; then
    echo "✓ output/ directory exists"
    
    if [ -f "output/index.html" ]; then
        echo "✓ Main site built (output/index.html)"
    else
        echo "✗ Main site missing!"
        exit 1
    fi
    
    if [ -d "output/v1" ]; then
        echo "✓ V1 docs preserved (output/v1/)"
    else
        echo "⚠ V1 docs not found (may not exist yet)"
    fi
    
    if [ -d "output/docs" ]; then
        echo "✓ V2 docs built with MkDocs (output/docs/)"
    else
        echo "✗ V2 docs missing!"
        exit 1
    fi
    
    # Count files
    file_count=$(find output -type f | wc -l)
    echo "✓ Total files in output: $file_count"
else
    echo "✗ output/ directory not found!"
    exit 1
fi

echo ""
echo "========================================="
echo "Build completed successfully!"
echo "========================================="
echo ""
echo "Output directory: output/"
echo "  - Main site: output/index.html"
echo "  - V1 docs: output/v1/"
echo "  - V2 docs: output/docs/ (with sidebar)"
echo ""

# Made with Bob
