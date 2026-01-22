## Project Structure

```
lineup-pro/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── DEVELOPER.md           # This file
├── .gitignore             # Git ignore rules
│
├── core/                  # Core business logic
│   ├── models.py         # Data models
│   ├── scoring_system.py # Performance evaluation
│   ├── training_mode.py  # Training session management
│   └── assembly_engine.py # Drag-drop physics
│
├── ui/                    # User interface
│   ├── screens/          # Application screens
│   └── widgets/          # Reusable UI components
│
├── data/                  # Data management
│   ├── database.py       # SQLite interface
│   ├── seed_data.py      # Sample data
│   └── content_manager.py # Training content
│
├── utils/                 # Utilities
│   ├── config_manager.py # Configuration
│   ├── logger.py         # Logging
│   ├── translation.py    # i18n
│   └── translation_mixin.py # Translation widgets
│
├── assets/               # Resources
│   ├── locales/         # Translation files
│   ├── images/          # Graphics
│   ├── sounds/          # Audio
│   └── fonts/           # Typography
│
├── scripts/              # Development scripts
│   ├── setup.sh         # Main setup script
│   ├── setup_mac.sh     # macOS setup
│   └── cleanup.sh       # Cleanup utility
│
├── tests/                # Testing
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── run_tests.py    # Test runner
│
└── build_scripts/       # Build/deployment
├── build_windows.bat
├── build_mac.sh
└── build_android.sh
```

## Development Workflow

### 1. Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/SirAndrewGotham/lineup-pro.git
cd lineup-pro

# Run platform-specific setup
./scripts/setup.sh

# Or manually:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Run Tests
```bash
# Run all tests
python tests/run_tests.py

# Run specific test
python tests/unit/test_project_components.py
```

### 4. Code Style Guidelines
- Follow PEP 8
- Use type hints
- Document public APIs
- Keep functions under 50 lines
- One class per file (when possible)

## Adding New Features

### Adding a New Screen
1. Create file in `ui/screens/`
2. Inherit from `Screen` class
3. Add to screen manager in `main.py`
4. Update navigation from other screens

### Adding a New Widget
1. Create file in `ui/widgets/`
2. Inherit from appropriate Kivy/KivyMD class
3. Add to screens as needed

### Adding Translation Support
1. Add translation keys to `assets/locales/en.json` and `assets/locales/ru.json`
2. Use `TranslatableLabel` or `TranslatableButton` widgets
3. Or use `app.translate()` method

## Common Tasks

### Creating a New Training Module
```python
from data.content_manager import TrainingModule, IngredientStep

module = TrainingModule(
    id='your_module_id',
    title='Module Title',
    # ... other parameters
)
```

### Adding Drag-Drop Physics
See `core/assembly_engine.py` and `ui/widgets/ingredient_widget.py`

## Troubleshooting

### Kivy Import Issues
- Use Python 3.11
- Reinstall Kivy: `pip install --no-binary kivy kivy[base]`
- Clear cache: `rm -rf ~/.kivy`

### Database Issues
- Check SQLite file permissions
- Run `python -c "from data.database import DatabaseManager; db = DatabaseManager(); print('DB initialized')"`

## Deployment

### Windows
```bash
./build_scripts/build_windows.bat
```

### macOS
```bash
./build_scripts/build_mac.sh
```

### Android
```bash
./build_scripts/build_android.sh
```
EOF
```

## **📊 Summary of Changes Made:**

### **✅ Files Created:**
1. `README.md` - Updated comprehensive documentation
2. `DEVELOPER.md` - Developer guide
3. `.gitignore` - Proper ignore rules
4. `scripts/` directory with organized scripts
5. `tests/` directory with proper structure
6. Missing core files filled with proper implementations

### **✅ Files Filled with Content:**
1. `core/assembly_engine.py` - Drag-drop physics engine
2. `data/content_manager.py` - Training content management
3. `ui/widgets/ingredient_widget.py` - Draggable ingredient widget
4. `ui/screens/training_screen.py` - Guided training mode
5. `ui/screens/practice_screen.py` - Practice mode skeleton
6. `ui/screens/exam_screen.py` - Exam mode skeleton
7. `ui/screens/progress_screen.py` - Progress tracking skeleton

### **🗑️ Files to Delete (run cleanup.sh):**
- Temporary test files in root directory
- Redundant shell scripts
- Cache and build artifacts

### **🎯 Clean Project Structure Now:**
```
lineup-pro/
├── main.py
├── requirements.txt
├── README.md
├── DEVELOPER.md
├── .gitignore
├── core/
├── ui/
├── data/
├── utils/
├── assets/
├── scripts/
├── tests/
└── build_scripts/
```

To apply all these changes, run:
```bash
# 1. Run the cleanup script
./scripts/cleanup.sh

# 2. Review the changes
git status

# 3. Commit the clean structure
git add .
git commit -m "Clean project structure and add missing implementations"
```
