#!/bin/bash
echo "Building LineUp Pro for Android..."

# Install Buildozer if not installed
pip install buildozer cython

# Create buildozer.spec if not exists
if [ ! -f "buildozer.spec" ]; then
    buildozer init
    # Update buildozer.spec with our settings
    cp build_scripts/buildozer_template.spec buildozer.spec
fi

# Clean previous builds
buildozer android clean

# Build APK
buildozer android debug

echo "Build complete! APK in bin directory.