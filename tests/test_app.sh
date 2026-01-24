#!/bin/bash
echo "=== LineUp Pro Application Test ==="
echo ""

# 1. Check Python version
echo "1. Python version:"
python3 --version
echo ""

# 2. Test all imports
echo "2. Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '.')

modules = [
    'main', 'utils.logger', 'core.training_mode',
    'utils.config_manager', 'data.database',
    'ui.screens.main_screen', 'ui.screens.settings_screen',
    'utils.translation', 'core.models', 'core.scoring_system'
]

for module in modules:
    try:
        __import__(module)
        print(f'  ✅ {module}')
    except ImportError as e:
        print(f'  ❌ {module}: {e.name if hasattr(e, \"name\") else str(e)}')
    except Exception as e:
        print(f'  ⚠️ {module}: {type(e).__name__}: {str(e)[:50]}')
"
echo ""

# 3. Try to create app instance
echo "3. Testing app instantiation..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from main import LineUpProApp
    app = LineUpProApp()
    print('  ✅ App instance created successfully')
    print(f'  App title: {app.title}')
except Exception as e:
    print(f'  ❌ Failed to create app: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
"
echo ""

# 4. Check if config gets created
echo "4. Checking configuration..."
if [ -f "config.json" ]; then
    echo "  ✅ config.json exists"
    echo "  Content preview:"
    python3 -c "import json; data = json.load(open('config.json')); print(json.dumps(data, indent=2)[:200])"
else
    echo "  ⚠️ config.json not found (will be created on first run)"
fi
echo ""

# 5. Check database
echo "5. Checking database..."
if [ -f "lineup_pro.db" ]; then
    echo "  ✅ lineup_pro.db exists"
    size=$(wc -c < "lineup_pro.db")
    echo "  Size: $((size/1024)) KB"
else
    echo "  ⚠️ lineup_pro.db not found (will be created on first run)"
fi
echo ""

echo "=== Test Complete ==="
