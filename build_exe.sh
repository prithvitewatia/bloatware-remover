#!/bin/bash
# Build script to create a standalone executable for bloatware-remove
# Requires: pyinstaller

set -e

# Ensure PyInstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build the executable
echo "Building the executable..."
pyinstaller \
--onefile src/main.py \
--name bloatware-remover \
--add-data "src/templates:src/templates"

echo "Build complete. The executable is in the dist/ directory."

