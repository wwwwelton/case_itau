#!/bin/bash

DEPENDENCIES_DIR="dependencies"
ZIP_FILE="function.zip"
ENTRY_POINT="."

mkdir -p $DEPENDENCIES_DIR

echo "Installing dependencies..."
pip install -r requirements.txt -t $DEPENDENCIES_DIR

echo "Zipping files..."
# zip -r $ZIP_FILE $ENTRY_POINT .
zip -r $ENTRY_POINT/$ZIP_FILE . -x ".aws-sam/*" "venv/*" "terraform/*" "function.zip" "README.md" "__pycache__/*" ".gitignore" ".env" "images/*" "setup.sh" ".git/*"

if [ -f "$ZIP_FILE" ]; then
  echo "Lambda package created successfully: $ZIP_FILE"
else
  echo "Failed to create Lambda package."
  exit 1
fi
