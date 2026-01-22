@echo off
echo Building LineUp Pro for Windows...

:: Create virtual environment
python -m venv build_venv
call build_venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
pip install pyinstaller

:: Create build directory
if not exist "dist\windows" mkdir "dist\windows"

:: Build with PyInstaller
pyinstaller --onefile ^
            --windowed ^
            --name "LineUpPro" ^
            --icon "assets\icons\app_icon.ico" ^
            --add-data "assets;assets" ^
            --add-data "*.kv;." ^
            main.py

echo Build complete! Check dist\windows folder.
pause
