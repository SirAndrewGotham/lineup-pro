#!/bin/bash
# setup_environment_mac.sh - For macOS with Apple Silicon/Intel

echo "Setting up LineUp Pro environment for macOS..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python 3.11 (compatible with Kivy)
echo "Installing Python 3.11..."
brew install python@3.11

# Install system dependencies for Kivy
echo "Installing Kivy dependencies..."
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
brew install ffmpeg libav

# Create virtual environment with Python 3.11
echo "Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install Kivy with macOS-specific options
echo "Installing Kivy..."
pip install "kivy[base]" --no-binary kivy

# Install other requirements
echo "Installing project requirements..."
pip install kivymd==1.2.0
pip install pillow
pip install pygments

# Install remaining requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Environment setup complete!"
echo "To activate the virtual environment: source venv/bin/activate"
echo "To run the app: python main.py"
