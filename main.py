# main.py - Fixed version
import kivy
kivy.require('2.3.0')

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import MDApp, fallback to regular App
try:
    from kivymd.app import MDApp
    KIVYMD_AVAILABLE = True
except ImportError:
    from kivy.app import App as MDApp
    KIVYMD_AVAILABLE = False
    print("Warning: KivyMD not available, using regular Kivy")

from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.logger import Logger

# Try to import all screens with fallbacks
try:
    from ui.screens.main_screen import MainScreen
    MAIN_SCREEN_IMPORTED = True
except ImportError as e:
    Logger.warning(f"MainScreen import failed: {e}")
    MAIN_SCREEN_IMPORTED = False

try:
    from ui.screens.settings_screen import SettingsScreen
    SETTINGS_SCREEN_IMPORTED = True
except ImportError as e:
    Logger.warning(f"SettingsScreen import failed: {e}")
    SETTINGS_SCREEN_IMPORTED = False

# Create fallback screens if imports fail
if not MAIN_SCREEN_IMPORTED:
    from kivy.uix.screenmanager import Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label

    class MainScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = 'main'
            layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
            layout.add_widget(Label(text='LineUp Pro', font_size=32))
            layout.add_widget(Button(text='Training (Coming Soon)'))
            layout.add_widget(Button(text='Practice (Coming Soon)'))
            layout.add_widget(Button(text='Settings', on_release=lambda x: setattr(self.manager, 'current', 'settings')))
            layout.add_widget(Button(text='Exit', on_press=lambda x: MDApp.get_running_app().stop()))
            self.add_widget(layout)

if not SETTINGS_SCREEN_IMPORTED:
    from kivy.uix.screenmanager import Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label

    class SettingsScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.name = 'settings'
            layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
            layout.add_widget(Label(text='Settings', font_size=32))
            layout.add_widget(Label(text='Language:'))
            lang_btn = Button(text='English')
            lang_btn.bind(on_release=lambda x: setattr(lang_btn, 'text', 'Русский' if lang_btn.text == 'English' else 'English'))
            layout.add_widget(lang_btn)
            layout.add_widget(Button(text='Back', on_press=lambda x: setattr(self.manager, 'current', 'main')))
            self.add_widget(layout)


class LineUpPro(MDApp):
    """Main application class for LineUp Pro training simulator"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "LineUp Pro - Interactive Training Simulator"
        self.theme_cls.theme_style = "Light"  # KivyMD theme
        self.theme_cls.primary_palette = "Blue"

    def build(self):
        """Build and return the root widget"""
        # Initialize configuration
        try:
            from utils.config_manager import ConfigManager
            self.config_manager = ConfigManager()
        except ImportError as e:
            Logger.warning(f"ConfigManager import failed: {e}")
            self.config_manager = None

        # Initialize translation system
        try:
            from utils.translation import TranslationManager
            self.translation_manager = TranslationManager()
        except ImportError as e:
            Logger.warning(f"TranslationManager import failed: {e}")
            self.translation_manager = None

        # Initialize database
        try:
            from data.database import DatabaseManager
            self.database = DatabaseManager()
        except ImportError as e:
            Logger.warning(f"DatabaseManager import failed: {e}")
            self.database = None

        # Create screen manager
        self.sm = ScreenManager()

        # Add screens
        self.sm.add_widget(MainScreen())
        self.sm.add_widget(SettingsScreen())

        # Set initial screen
        self.sm.current = 'main'

        return self.sm

    def translate(self, key, **kwargs):
        """Translate a key using the current language"""
        if self.translation_manager:
            return self.translation_manager.translate(key, **kwargs)
        return key

    def on_stop(self):
        """Clean up when app stops"""
        if hasattr(self, 'database') and self.database:
            self.database.close_all_connections()


if __name__ == '__main__':
    # Set window size for development
    Window.size = (800, 600)

    # Run the application
    app = LineUpPro()
    app.run()
