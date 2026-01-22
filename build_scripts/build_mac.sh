#!/bin/bash
echo "Building LineUp Pro for macOS..."

# Create virtual environment
python3 -m venv build_venv
source build_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install py2app

# Create setup.py for py2app
cat > setup.py << 'EOF'
from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('assets', ['assets/images/*', 'assets/sounds/*', 'assets/fonts/*']),
    ('ui', ['ui/*.py', 'ui/screens/*.py', 'ui/widgets/*.py']),
    ('core', ['core/*.py']),
    ('data', ['data/*.py']),
    ('utils', ['utils/*.py'])
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['kivy', 'kivymd', 'sqlite3'],
    'plist': {
        'CFBundleName': 'LineUp Pro',
        'CFBundleDisplayName': 'LineUp Pro',
        'CFBundleIdentifier': 'com.vkusno.lineuppro',
        'CFBundleVersion': '0.1.0',
        'NSHumanReadableCopyright': '© 2024 Vkusno i tochka'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

# Build the application
python setup.py py2app

echo "Build complete! Check dist folder for LineUp Pro.app
