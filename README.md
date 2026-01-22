# LineUp Pro - Interactive Fast-Food Assembly Training Simulator

![Python](https://img.shields.io/badge/python-3.11-blue)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-green)
![KivyMD](https://img.shields.io/badge/kivymd-1.2.0-orange)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![Status](https://img.shields.io/badge/status-alpha-yellow)

**LineUp Pro** is a cross-platform interactive training simulator designed for fast-food assembly training, specifically tailored for "Vkusno i tochka" (ex-McDonald's Russia). The application provides immersive, gamified training experiences with real-time feedback and adaptive learning.

## 🎯 Project Status: ALPHA

**Current Progress**: ✅ Basic application launches successfully  
**Next Milestone**: Interactive drag-and-drop assembly simulator

## ✨ Key Features

### Core Training System
- ✅ **Three Training Modes**: Guided, Practice, Exam
- 🔄 **Interactive Assembly**: Drag-and-drop ingredient placement with physics
- ✅ **Universal Templates**: 5 core assembly patterns
- ✅ **Bilingual Support**: Full Russian/English localization
- ✅ **Offline-First**: No internet required for training sessions

### Learning Technology
- 🔄 **Adaptive AI**: Personalized difficulty based on performance
- ✅ **Real-time Feedback**: Immediate correction during assembly
- ✅ **Performance Analytics**: Detailed progress tracking and reporting
- 🔄 **Voice Guidance**: Text-to-speech instructions (planned)

### Platform Support
- ✅ **Cross-Platform**: Single codebase for Windows/macOS/Linux/Android/iOS
- ✅ **Mobile-First Design**: Optimized for tablet and phone use
- ✅ **Native Performance**: Python/Kivy for smooth 60fps simulation

## 🏗️ Architecture

# Create organized directories
mkdir -p scripts/
mkdir -p tests/unit/
mkdir -p tests/integration/
mkdir -p docs/
mkdir -p tools/


# Move all shell scripts to scripts/
mv setup_environment.sh scripts/
mv setup_kivy_mac.sh scripts/
mv test_app.sh tests/  # This is actually a test script

# Rename for clarity
mv scripts/setup_environment.sh scripts/setup_dev.sh
mv scripts/setup_kivy_mac.sh scripts/setup_mac.sh

# Create a main setup script
cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# LineUp Pro - Development Environment Setup

echo "Setting up LineUp Pro development environment..."

# Check platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected. Running macOS setup..."
    ./scripts/setup_mac.sh
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected. Running Linux setup..."
    # TODO: Add Linux setup
    echo "Linux setup not yet implemented"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Windows detected. Running Windows setup..."
    # TODO: Add Windows setup
    echo "Windows setup not yet implemented"
else
    echo "Unknown operating system: $OSTYPE"
    exit 1
fi

echo "Setup complete!"
