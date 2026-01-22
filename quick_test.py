#!/usr/bin/env python3
"""
Quick test script for LineUp Pro
Run with: python quick_test.py
"""

import sys
import os
import json
import sqlite3
from pathlib import Path
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("1. Testing imports...")

    modules_to_test = [
        ('main', 'LineUpProApp'),
        ('utils.logger', 'setup_logging'),
        ('core.training_mode', 'TrainingSessionManager'),
        ('utils.config_manager', 'ConfigManager'),
        ('data.database', 'DatabaseManager'),
        ('ui.screens.main_screen', 'MainScreen'),
        ('ui.screens.settings_screen', 'SettingsScreen'),
        ('utils.translation', 'translation_manager'),
        ('core.models', 'TrainingMode'),
        ('core.scoring_system', 'ScoringSystem'),
    ]

    success = True
    for module_name, class_name in modules_to_test:
        try:
            exec(f'from {module_name} import {class_name}')
            print(f"  ✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ❌ {module_name}.{class_name}: {type(e).__name__}")
            print(f"      Error: {str(e)[:100]}")
            success = False

    return success

def test_app_instantiation():
    """Test that the app can be instantiated"""
    print("\n2. Testing app instantiation...")
    try:
        from main import LineUpProApp
        app = LineUpProApp()
        print(f"  ✅ App instance created")
        print(f"  Title: {app.title}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create app: {type(e).__name__}")
        print(f"  Error: {str(e)[:200]}")
        traceback.print_exc(limit=1)
        return False

def test_configuration():
    """Test configuration files"""
    print("\n3. Checking configuration...")

    config_path = Path("config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"  ✅ config.json exists")
            print(f"  Language: {config.get('ui', {}).get('language', 'not set')}")
            return True
        except Exception as e:
            print(f"  ❌ config.json is invalid: {e}")
            return False
    else:
        print("  ⚠️ config.json not found (will be created on first run)")
        return True  # Not an error, will be created

def test_database():
    """Test database file"""
    print("\n4. Checking database...")

    db_path = Path("lineup_pro.db")
    if db_path.exists():
        try:
            # Try to connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            print(f"  ✅ lineup_pro.db exists")
            print(f"  Size: {db_path.stat().st_size / 1024:.1f} KB")
            print(f"  Tables: {len(tables)}")

            conn.close()
            return True
        except Exception as e:
            print(f"  ❌ Database error: {e}")
            return False
    else:
        print("  ⚠️ lineup_pro.db not found (will be created on first run)")
        return True  # Not an error, will be created

def test_assets():
    """Check required asset directories"""
    print("\n5. Checking assets...")

    required_dirs = [
        "assets/images",
        "assets/locales",
        "assets/sounds",
        "assets/fonts",
        "logs"
    ]

    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ⚠️ {dir_path}/ (missing)")
            all_exist = False

    # Check translation files
    locale_files = list(Path("assets/locales").glob("*.json"))
    if locale_files:
        print(f"  ✅ Translation files: {len(locale_files)}")
    else:
        print("  ⚠️ No translation files found")

    return all_exist

def main():
    """Run all tests"""
    print("=" * 50)
    print("LineUp Pro - Application Test")
    print("=" * 50)

    # Add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))

    tests = [
        ("Imports", test_imports),
        ("App Instantiation", test_app_instantiation),
        ("Configuration", test_configuration),
        ("Database", test_database),
        ("Assets", test_assets),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Application is ready.")
        return 0
    else:
        print("⚠️ Some tests failed. Check above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
