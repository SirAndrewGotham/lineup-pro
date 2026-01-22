#!/usr/bin/env python3
"""
LineUp Pro - Test Runner
Run all tests with: python tests/run_tests.py
"""

import sys
import os
import unittest
import subprocess

def run_shell_tests():
    """Run shell-based tests"""
    print("=== Running Shell Tests ===")
    scripts = [
        'test_app.sh',
    ]
    
    for script in scripts:
        script_path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(script_path):
            print(f"\nRunning {script}...")
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Errors: {result.stderr}")

def run_python_tests():
    """Run Python unit tests"""
    print("\n=== Running Python Unit Tests ===")
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'unit')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("LineUp Pro - Test Suite")
    print("=" * 50)
    
    run_shell_tests()
    python_success = run_python_tests()
    
    print("\n" + "=" * 50)
    if python_success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
