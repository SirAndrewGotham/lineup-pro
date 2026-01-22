#!/bin/bash
# Cleanup temporary and unnecessary files

echo "Cleaning up project directory..."

# List of files to delete (temporary/test files)
files_to_delete=(
    "test_kivy_basic.py"
    "simple_working_app.py"
    "working_app.py"
    "create_placeholder_logo.py"
    "debug_main.py"
    "check_translation_mixin.py"
    ".DS_Store"  # macOS junk
)

# List of files to move (if they exist in root)
files_to_move=(
    "test_app.sh:tests/"
    "setup_environment.sh:scripts/"
    "setup_kivy_mac.sh:scripts/"
)

# Delete temporary files
for file in "${files_to_delete[@]}"; do
    if [ -f "$file" ]; then
        echo "Deleting: $file"
        rm "$file"
    fi
done

# Move files to appropriate directories
for mapping in "${files_to_move[@]}"; do
    src="${mapping%:*}"
    dest="${mapping#*:}"
    
    if [ -f "$src" ]; then
        echo "Moving: $src -> $dest"
        mkdir -p "$dest"
        mv "$src" "$dest"
    fi
done

# Clean __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

echo "Cleanup complete!"
