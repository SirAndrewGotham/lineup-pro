# LineUp Pro - Interactive Fast-Food Assembly Training Simulator

![Python](https://img.shields.io/badge/python-3.11-blue)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-green)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![Status](https://img.shields.io/badge/status-alpha-yellow)
![Database](https://img.shields.io/badge/database-sqlite-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**LineUp Pro** is a cross-platform interactive training simulator designed for fast-food assembly training, specifically tailored for "Vkusno i tochka" (ex-McDonald's Russia). The application provides immersive, gamified training experiences with real-time feedback and adaptive learning.

## 🎯 Project Status: ALPHA

**Current Progress**: ✅ Basic application launches successfully  
**Next Milestone**: Interactive drag-and-drop assembly simulator

## ✨ Key Features

### ✅ **Implemented Features**
- **Three Training Modes**: Guided, Practice, Exam (skeleton implemented)
- **Flashcards System**: Dish memorization with flip animation
- **Universal Templates**: 5 core assembly patterns in database
- **Bilingual Support**: Full Russian/English localization
- **Offline-First**: No internet required for training sessions
- **Cross-Platform**: Windows/macOS/Linux/Android/iOS ready
- **Mobile-First Design**: Optimized for tablet and phone use
- **Performance Tracking**: SQLite-based progress monitoring

### 🔄 **In Progress**
- **Interactive Assembly**: Drag-and-drop ingredient placement
- **Adaptive AI**: Personalized difficulty algorithms
- **Voice Guidance**: Text-to-speech instructions

### 📋 **Planned Features**
- **AR Integration**: Camera-based assembly verification
- **Multiplayer**: Competitive training challenges
- **Admin Dashboard**: Trainer content management

## 🏗️ Architecture

### **Technology Stack**
```
Frontend:     Kivy 2.3.0 (Python GUI Framework)
Database:     SQLite 3 (Local storage)
Localization: JSON-based i18n (Russian/English)
Build Tools:  PyInstaller (Desktop) / Buildozer (Mobile)
Testing:      pytest (Unit & Integration tests)
```

### **Project Structure**
```
lineup-pro/
├── core/                    # Core application logic
│   ├── models.py           # Data models (Ingredients, Templates, Flashcards)
│   ├── scoring_system.py   # Performance evaluation
│   ├── training_mode.py    # Training session manager
│   └── assembly_engine.py  # Assembly simulation engine
├── ui/                     # User interface
│   ├── screens/
│   │   ├── main_screen.py           # Main menu
│   │   ├── training_screen.py       # Guided training
│   │   ├── practice_screen.py       # Practice mode
│   │   ├── exam_screen.py           # Exam mode
│   │   ├── flashcards_screen.py     # NEW: Dish memorization
│   │   ├── progress_screen.py       # Analytics dashboard
│   │   └── settings_screen.py       # App settings
│   ├── widgets/
│   │   ├── assembly_area.py         # Drag-drop simulator
│   │   ├── flashcard_widget.py      # NEW: Interactive flashcards
│   │   └── ingredient_widget.py     # Ingredient UI components
│   └── styles/             # UI themes and styling
├── data/                   # Data management
│   ├── database.py        # SQLite interface
│   ├── seed_data.py       # Universal templates (5 patterns)
│   ├── seed_flashcards.py # NEW: Flashcards seed data
│   └── content_manager.py # Training content loader
├── utils/                  # Utilities
│   ├── config_manager.py  # Configuration system
│   ├── logger.py          # Logging system
│   ├── translation.py     # Russian/English i18n
│   └── translation_mixin.py # Kivy translation support
├── assets/                # Media resources
│   ├── locales/           # Translation files
│   │   ├── en.json
│   │   └── ru.json
│   ├── images/            # UI graphics and dish images
│   ├── sounds/            # Audio feedback
│   └── fonts/             # Typography
├── build_scripts/         # Platform builds
│   ├── build_windows.bat
│   ├── build_android.sh
│   ├── build_mac.sh
│   └── buildozer_template.spec
├── scripts/               # Development tools
│   ├── setup.sh           # Environment setup
│   ├── setup_mac.sh       # macOS specific setup
│   └── setup_dev.sh       # Development setup
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── test_app.sh        # Application test script
│   └── quick_test.py      # Quick test runner
├── docs/                  # Documentation
├── tools/                 # Development tools
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### **Quick Installation**
```bash
# Clone the repository
git clone https://github.com/sirandrewgotham/lineup-pro.git
cd lineup-pro

# Setup development environment
chmod +x scripts/setup.sh
./scripts/setup.sh

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from data.database import DatabaseManager; db = DatabaseManager(); db.initialize()"

# Seed flashcards data
python data/seed_flashcards.py

# Run the application
python main.py
```

### **Platform-Specific Setup**

#### **macOS**
```bash
./scripts/setup_mac.sh
```

#### **Linux**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

#### **Windows**
```bash
# Requires Python 3.8+ installed from python.org
# Run as Administrator for best results
```

## 📱 Features in Detail

### **1. Training Modes**
- **Guided Mode**: Step-by-step instructions with visual hints
- **Practice Mode**: Timed practice with error feedback
- **Exam Mode**: Strict timing and professional scoring
- **Flashcards Mode**: NEW! Dish memorization with interactive cards

### **2. Flashcards System** 🆕
- **Interactive Cards**: Flip animation for dish ingredients
- **Categorization**: Filter by dish type (sandwiches, sides, desserts)
- **Difficulty Levels**: Easy, medium, hard
- **Progress Tracking**: Mastery level and review count
- **Translation Ready**: Full Russian/English support

### **3. Assembly Simulation**
- Drag-and-drop ingredient placement
- Real-time physics simulation
- Visual feedback (correct/incorrect highlighting)
- Haptic feedback on mobile devices
- Voice-guided instructions

### **4. Performance Analytics**
- Real-time scoring during assembly
- Accuracy and speed metrics
- Progress tracking over time
- Skill matrix visualization
- Common error patterns

## 🗄️ Database Schema

The application uses SQLite with the following key tables:
- `templates`: Sandwich assembly templates
- `ingredients`: Ingredient definitions
- `training_sessions`: Session records
- `user_progress`: Performance analytics
- `flashcards`: NEW! Dish memorization cards

## 🌐 Localization

Full bilingual support with easy extension:
- English (`assets/locales/en.json`)
- Russian (`assets/locales/ru.json`)
- JSON-based translation system
- Runtime language switching

## 🛠️ Development

### **Running Tests**
```bash
# Quick test
python tests/quick_test.py

# Run all tests
./tests/test_app.sh

# Unit tests
python -m pytest tests/unit/
```

### **Building for Platforms**

#### **Desktop (Windows/macOS/Linux)**
```bash
# Windows
./build_scripts/build_windows.bat

# macOS
./build_scripts/build_mac.sh

# Linux
chmod +x build_scripts/build_linux.sh
./build_scripts/build_linux.sh
```

#### **Mobile (Android)**
```bash
chmod +x build_scripts/build_android.sh
./build_scripts/build_android.sh
```

### **Code Style**
- Follow PEP 8 guidelines
- Use type hints for better code clarity
- Document public methods with docstrings
- Keep functions focused and single-purpose

## 📊 Current Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Core Models | ✅ Complete | All data models implemented |
| Database | ✅ Complete | SQLite with all tables |
| Main UI | ✅ Complete | Main menu and navigation |
| Settings | ✅ Complete | Language switching |
| Flashcards | ✅ Complete | Interactive card system |
| Assembly Sim | 🔄 In Progress | Drag-drop implementation |
| Training Modes | 🔄 In Progress | Guided/Practice/Exam screens |
| Scoring System | ⏳ Planned | Real-time performance evaluation |
| Analytics Dashboard | ⏳ Planned | Progress visualization |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Development Guidelines**
- Write tests for new features
- Update documentation accordingly
- Follow existing code style
- Add translations for new UI text

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kivy Team** for the excellent cross-platform framework
- **SQLite** for reliable local data storage
- **Python Community** for extensive library support
- **Fast-food training professionals** for domain expertise

## 📞 Support

For issues, feature requests, or questions:
1. Check the [Issues](https://github.com/sirandrewgotham/lineup-pro/issues) page
2. Review the [Documentation](docs/) folder
3. Contact the maintainer via GitHub

---

**LineUp Pro** - Making fast-food training faster, smarter, and more engaging since 2024. 🍔🎯
