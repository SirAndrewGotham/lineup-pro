# test_full_app.py
import sys
import os

print("=== LineUp Pro Installation Test ===\n")

# Test 1: Check Python and imports
print("1. Python Environment:")
print(f"   Python: {sys.version}")
print(f"   Working dir: {os.getcwd()}")

# Test 2: Check Kivy imports
try:
    import kivy
    import kivymd
    print(f"   ✓ Kivy: {kivy.__version__}")
    print(f"   ✓ KivyMD: {kivymd.__version__}")
except ImportError as e:
    print(f"   ✗ Import error: {e}")

# Test 3: Check project imports
print("\n2. Project Imports:")
modules_to_test = [
    'utils.config_manager',
    'utils.translation',
    'data.database',
    'ui.screens.main_screen',
    'ui.screens.settings_screen'
]

for module in modules_to_test:
    try:
        __import__(module.replace('/', '.'))
        print(f"   ✓ {module}")
    except ImportError as e:
        print(f"   ✗ {module}: {e}")

# Test 4: Check translation files
print("\n3. Translation Files:")
if os.path.exists('assets/locales'):
    for file in os.listdir('assets/locales'):
        if file.endswith('.json'):
            size = os.path.getsize(f'assets/locales/{file}')
            print(f"   ✓ {file} ({size} bytes)")
else:
    print("   ✗ assets/locales directory not found")

print("\n=== Test Complete ===")
print("\nTo run the app:")
print("1. Fix utils/translation_mixin.py (add missing classes)")
print("2. Run: python main.py")
