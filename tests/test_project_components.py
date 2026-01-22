# test_project_components.py
import sys
import os
import sqlite3
import json

def test_project_structure():
    """Test if project directories and files exist"""
    print("=== Testing Project Structure ===")

    required_dirs = ['core', 'ui', 'data', 'utils', 'assets']
    for dir_name in required_dirs:
        exists = os.path.exists(dir_name)
        print(f"{dir_name}: {'✓' if exists else '✗'}")
        if exists:
            print(f"  Contents: {os.listdir(dir_name)}")

    required_files = ['main.py', 'requirements.txt']
    for file_name in required_files:
        exists = os.path.exists(file_name)
        print(f"{file_name}: {'✓' if exists else '✗'}")

def test_database():
    """Test SQLite database connection"""
    print("\n=== Testing Database ===")
    try:
        # Try to access the database
        from data.database import DatabaseManager
        db = DatabaseManager()
        print("✓ DatabaseManager imported successfully")

        # Test connection
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✓ Database connected. Tables found: {[t[0] for t in tables]}")
        conn.close()
    except Exception as e:
        print(f"✗ Database error: {e}")

def test_kivy_components():
    """Test Kivy and KivyMD imports"""
    print("\n=== Testing Kivy Components ===")

    try:
        import kivy
        print(f"✓ Kivy: {kivy.__version__}")
    except ImportError as e:
        print(f"✗ Kivy import failed: {e}")

    try:
        import kivymd
        print(f"✓ KivyMD imported")
    except ImportError as e:
        print(f"✗ KivyMD import failed: {e}")

    try:
        from kivy.uix.screenmanager import ScreenManager
        print("✓ Kivy ScreenManager imported")
    except ImportError as e:
        print(f"✗ Kivy component import failed: {e}")

def test_translation_system():
    """Test translation files"""
    print("\n=== Testing Translation System ===")

    locale_path = '../assets/locales'
    if os.path.exists(locale_path):
        files = os.listdir(locale_path)
        print(f"✓ Locales directory exists. Files: {files}")

        # Test loading a translation file
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(locale_path, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(f"✓ {file}: Loaded {len(data)} translation keys")
                except Exception as e:
                    print(f"✗ {file}: Failed to load - {e}")
    else:
        print("✗ Locales directory not found")

def test_main_app():
    """Test if main app can be imported"""
    print("\n=== Testing Main Application ===")

    try:
        # Check if main.py exists and can be parsed
        with open('../main.py', 'r') as f:
            content = f.read()
            if 'class LineUpPro' in content or 'class MainApp' in content:
                print("✓ Main application class found in main.py")
            else:
                print("⚠ Main application class not found in main.py")
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")

if __name__ == '__main__':
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}\n")

    test_project_structure()
    test_database()
    test_kivy_components()
    test_translation_system()
    test_main_app()

    print("\n=== Summary ===")
    print("If you see mostly ✓ marks, your installation is working!")
    print("To run the actual app: python main.py")
