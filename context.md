```
"I am developing a cross-platform training simulator for fast-food assembly. 
Please help me implement this Python/Kivy application according to the 
specifications in the attached document. Let's start with the core architecture."
```

# **Project Proposal: "LineUp Pro" - Cross-Platform Interactive Training Simulator** - UPDATED

## **Executive Summary**
**Project Name:** LineUp Pro (Codename: AssemblyMaster)
**Type:** Cross-platform interactive training simulator for fast-food assembly
**Target:** "Vkusno i tochka" (ex-McDonald's Russia) kitchen staff training
**Approach:** Python-based desktop/mobile app with eventual web deployment
**Core Innovation:** Gamified assembly simulation with adaptive learning AI + Flashcards system

## **Updated Technology Stack:**
```
Primary Framework: Kivy 2.3.0 (Implemented - NOT using KivyMD)
Python: 3.11+ (with compatibility adjustments)
Database: SQLite (fully implemented with flashcards support)
Translation: JSON-based system with Russian/English support + TranslationMixin
UI Framework: Pure Kivy with custom Translatable widgets
```

### **Updated Project Structure:**
```
lineup-pro/ (ACTUAL - GitHub: https://github.com/SirAndrewGotham/lineup-pro)
├── core/                    # ✅ IMPLEMENTED
│   ├── models.py           # ✅ Data models (now includes Flashcard model)
│   ├── scoring_system.py   # ⏳ TODO (not yet implemented)
│   ├── training_mode.py    # ⏳ TODO (not yet implemented)
│   └── assembly_engine.py  # ⏳ TODO (not yet implemented)
├── ui/                     # ✅ PARTIALLY IMPLEMENTED
│   ├── screens/
│   │   ├── main_screen.py           # ✅ WITH FLASHCARDS BUTTON
│   │   ├── training_screen.py       # ⏳ SKELETON
│   │   ├── practice_screen.py       # ⏳ SKELETON
│   │   ├── exam_screen.py           # ⏳ SKELETON
│   │   ├── flashcards_screen.py     # ✅ NEW - IMPLEMENTED
│   │   ├── progress_screen.py       # ⏳ SKELETON
│   │   └── settings_screen.py       # ✅ WITH LANGUAGE SUPPORT
│   ├── widgets/
│   │   ├── assembly_area.py         # ⏳ TODO (not yet implemented)
│   │   ├── ingredient_widget.py     # ⏳ TODO (not yet implemented)
│   │   └── flashcard_widget.py      # ✅ NEW - IMPLEMENTED
│   └── styles/             # ⏳ TODO
├── data/                  # ✅ UPDATED
│   ├── database.py       # ✅ SQLite interface (needs flashcards methods)
│   ├── seed_data.py      # ✅ Universal templates (5 patterns)
│   ├── seed_flashcards.py # ✅ NEW - IMPLEMENTED
│   └── content_manager.py # ⏳ TODO
├── utils/                 # ✅ IMPLEMENTED
│   ├── config_manager.py # ✅ Configuration system
│   ├── logger.py         # ✅ Logging system
│   ├── translation.py    # ✅ Russian/English i18n
│   └── translation_mixin.py # ✅ Kivy translation support
├── assets/               # ⏳ UPDATED
│   ├── locales/          # ✅ en.json, ru.json (updated with flashcards keys)
│   ├── images/           # ⏳ EMPTY (placeholders needed for flashcards)
│   ├── sounds/           # ⏳ EMPTY
│   └── fonts/            # ⏳ EMPTY
├── build_scripts/        # ✅ IMPLEMENTED
│   ├── build_windows.bat
│   ├── build_android.sh
│   ├── build_mac.sh
│   └── buildozer_template.spec
├── tests/                # ✅ ADDED
│   ├── test_app.sh       # ✅ Shell test script
│   └── quick_test.py     # ✅ Python test script
└── main.py               # ✅ APPLICATION ENTRY POINT (needs flashcards screen registration)
```

## **Updated Feature Specification**

### **✅ NEW FEATURE: Flashcards System**
**Interactive Memorization Tool:**
- Flip animation cards for dish ingredients
- Front side: Dish name only (prompts user to recall ingredients)
- Back side: Dish image + ingredient list + assembly tips
- Category filtering (sandwiches, sides, desserts, breakfast)
- Difficulty levels (easy, medium, hard)
- Progress tracking (mastery level, times reviewed)
- Translation support for all dish names and ingredients

**Three Training Modes (Updated):**
```
A. GUIDED MODE
   - Step-by-step instructions
   - Visual highlighting of next ingredient
   - Unlimited time, focus on accuracy

B. PRACTICE MODE
   - Timer visible but not restrictive
   - Error tracking with suggestions
   - Performance score at completion

C. EXAM MODE
   - Strict timer (realistic time limits)
   - No hints or corrections
   - Professional scoring (accuracy + speed)
   - Certification upon mastery

D. FLASHCARDS MODE 🆕
   - Dish memorization through active recall
   - Interactive flip cards
   - Progress-based difficulty adjustment
   - Prepares users for assembly training
```

### **✅ COMPLETED (Updated):**
- Project structure and virtual environment setup
- Kivy UI framework with main menu and settings
- SQLite database with schema and seed data
- **Flashcards feature complete** (models, UI, seed data)
- Translation system (Russian/English) with flashcards support
- Configuration management
- Build scripts for Windows/macOS/Android
- Test scripts for verification
- Custom translation widgets (TranslatableLabel, TranslatableButton)

### **🔄 IN PROGRESS (Updated):**
- Database methods for flashcards (needs implementation)
- Registration of flashcards screen in main.py
- Asset creation for flashcards (dish images)

### **⏳ TODO (Updated):**
- Drag-and-drop assembly simulator
- Three training modes implementation
- Assembly engine physics
- Progress tracking UI
- Advanced features (AI, voice, etc.)

## **Updated Implementation Status**

### **Phase 1: MVP (Current Status)**
```
Week 1-2: ✅ Core Architecture
    - ✅ Kivy app skeleton
    - ✅ SQLite database with universal templates
    - ✅ Flashcards system implemented
    - ✅ Translation system with Russian/English

Week 3-4: 🔄 Training Engine
    - ⏳ Three training modes implementation
    - ⏳ Scoring system
    - ⏳ Progress tracking
    - ✅ Flashcards mode COMPLETE

Week 5-6: ⏳ Polish & Content
    - ⏳ UI/UX refinement
    - ⏳ Sample training modules
    - ⏳ Basic reporting
```

### **Technical Debt/Issues to Fix:**
1. **Database methods missing** for flashcards CRUD operations
2. **Main.py needs updating** to register FlashcardsScreen
3. **Flashcard widget translation** needs integration with existing system
4. **Asset images missing** for dish visualization

## **Updated Success Metrics**

### **Technical Success:**
- Frame rate >60fps on simulation
- Launch time <3 seconds
- Memory usage <200MB
- Battery impact minimal on mobile
- **Flashcards load instantly** with smooth animations

### **Training Effectiveness:**
- 30% faster skill acquisition vs traditional training
- 95% user satisfaction rate
- 40% reduction in real-world errors
- Average daily usage >15 minutes
- **Flashcards mastery** correlates with assembly accuracy

## **Updated Next Steps**

### **Immediate Tasks:**
1. **Fix Database**: Add flashcard methods to database.py
2. **Register Screen**: Add FlashcardsScreen to main.py screen manager
3. **Asset Creation**: Add placeholder dish images
4. **Translation Integration**: Connect flashcard widget to translation system
5. **Test Flashcards**: Run complete test of flashcards feature

### **Priority Order:**
1. Complete flashcards database integration
2. Register and test flashcards screen
3. Add missing dish images (placeholders)
4. Implement drag-drop assembly simulator
5. Complete training mode screens

### **Decision Points (Updated):**
- ✅ Kivy selected (NOT KivyMD)
- ✅ Local-only architecture with SQLite
- ✅ Custom translation system implemented
- ⏳ Asset creation strategy (placeholders vs real images)
- ⏳ Scoring algorithm for flashcards mastery

## **Key Changes from Original Specification**

1. **Removed KivyMD**: Using pure Kivy with custom translation widgets
2. **Added Flashcards**: Complete new feature for dish memorization
3. **Updated Models**: Flashcard dataclass added to core/models.py
4. **Enhanced Translation**: Added dish and ingredient translation keys
5. **UI Structure**: Main menu now includes flashcards button
6. **Database Schema**: Flashcards table needs to be added

## **Risk Assessment**

### **Low Risk (Implemented):**
- Core architecture stable
- Translation system working
- Basic navigation functional
- Flashcards UI complete

### **Medium Risk (Needs Work):**
- Database integration for flashcards
- Asset management for dish images
- Screen registration in main app

### **High Risk (Not Started):**
- Drag-and-drop physics engine
- Real-time scoring system
- Training mode implementations

