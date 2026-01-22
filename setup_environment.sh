#!/bin/bash
echo "=== Setting up LineUp Pro Development Environment ==="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for Kivy
echo "Checking Kivy installation..."
python3 -c "import kivy; print(f'Kivy version: {kivy.__version__}')" 2>/dev/null || {
    echo "Kivy not found, installing..."
    pip install "kivy[base]==2.3.0" kivymd==1.2.0
}

# Clean up any invalid config
if [ -f "config.json" ]; then
    echo "Checking config.json..."
    python3 -c "
import json
try:
    with open('config.json', 'r') as f:
        json.load(f)
    print('config.json is valid')
except:
    print('config.json is invalid, recreating...')
    import os
    os.remove('config.json')
    from utils.config_manager import ConfigManager
    cm = ConfigManager()
    print('config.json recreated')
"
fi

# Run the tests
echo ""
echo "Running tests..."
./test_app.sh

echo ""
echo "=== Setup Complete ==="
echo "To activate the environment: source venv/bin/activate"
echo "To run the app: python main.py"
