"""
LineUp Pro - Cross-Platform Fast-Food Training Simulator
Entry point with complete application integration
"""

import os
import sys
from ui.screens.settings_screen import SettingsScreen
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Kivy configuration before importing
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Only set these if on mobile
if hasattr(sys, 'getandroidapilevel'):
    Config.set('kivy', 'exit_on_escape', '0')
    Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
import logging

# Import screens
from ui.screens.main_screen import MainScreen
from ui.screens.training_screen import TrainingScreen
from ui.screens.practice_screen import PracticeScreen
from ui.screens.exam_screen import ExamScreen
from ui.screens.progress_screen import ProgressScreen

# Import core components
from data.database import DatabaseManager
from utils.config_manager import ConfigManager
from utils.logger import setup_logging

class LineUpProApp(App):
    """Main application class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(__name__)

        # Initialize managers
        self.config = ConfigManager()
        self.db = DatabaseManager(
            db_path=self.config.get('paths.database', 'lineup_pro.db')
        )

        # Application state
        self.current_user = "default_user"
        self.current_session = None
        self.screen_manager = None

        self.logger.info("LineUp Pro application initialized")

    def build(self):
        """Build the application UI"""
        self.title = self.config.get('app.name', 'LineUp Pro')

        try:
            # Initialize database
            self.db.initialize()

            # Create screen manager
            self.screen_manager = ScreenManager(transition=FadeTransition())

            # Load KV files if any
            self.load_kv_files()

            # Create and add screens
            self.setup_screens()

            # Setup window for desktop
            if not hasattr(sys, 'getandroidapilevel'):
                self.setup_desktop_window()

            self.logger.info("Application UI built successfully")
            return self.screen_manager

        except Exception as e:
            self.logger.error(f"Error building application: {e}")
            raise

    def load_kv_files(self):
        """Load Kivy language files"""
        kv_files = [
            'ui/styles/themes.kv',
            'ui/screens/main_screen.kv',
            'ui/screens/training_screen.kv'
        ]

        for kv_file in kv_files:
            kv_path = Path(kv_file)
            if kv_path.exists():
                try:
                    Builder.load_file(str(kv_path))
                    self.logger.debug(f"Loaded KV file: {kv_file}")
                except Exception as e:
                    self.logger.warning(f"Could not load KV file {kv_file}: {e}")

    def setup_screens(self):
        """Initialize and add all screens"""
        screens = [
            ('main', MainScreen(name='main')),
            ('training', TrainingScreen(name='training')),
            ('practice', PracticeScreen(name='practice')),
            ('exam', ExamScreen(name='exam')),
            ('progress', ProgressScreen(name='progress')),
            ('settings', SettingsScreen(name='settings'))
        ]

        for screen_name, screen in screens:
            screen.app = self  # Pass app reference to screen
            self.screen_manager.add_widget(screen)

        # Set initial screen
        self.screen_manager.current = 'main'

    def setup_desktop_window(self):
        """Configure window for desktop platforms"""
        Window.size = (360, 640)
        Window.minimum_width = 360
        Window.minimum_height = 640

        # Set window icon if exists
        icon_path = Path('assets/icons/app_icon.png')
        if icon_path.exists():
            try:
                Window.set_icon(str(icon_path))
            except:
                pass  # Icon setting might fail on some platforms

    def start_training_session(self, template_id: str, mode: str):
        """Start a new training session"""
        from core.training_mode import TrainingSessionManager

        try:
            self.current_session = TrainingSessionManager(
                app=self,
                user_id=self.current_user,
                template_id=template_id,
                mode=mode
            )
            self.logger.info(f"Started {mode} session for template {template_id}")
            return self.current_session
        except Exception as e:
            self.logger.error(f"Error starting training session: {e}")
            return None

    def get_user_progress(self) -> dict:
        """Get current user's progress"""
        try:
            progress = self.db.get_user_progress(self.current_user)
            if progress:
                return progress.__dict__
            return {}
        except Exception as e:
            self.logger.error(f"Error getting user progress: {e}")
            return {}

    def get_available_templates(self, **filters):
        """Get available training templates"""
        try:
            return self.db.get_all_templates(**filters)
        except Exception as e:
            self.logger.error(f"Error getting templates: {e}")
            return []

    def switch_screen(self, screen_name: str):
        """Switch to another screen"""
        if self.screen_manager and screen_name in self.screen_manager.screen_names:
            self.screen_manager.current = screen_name
            self.logger.debug(f"Switched to screen: {screen_name}")

    def on_pause(self):
        """Pause the application (mobile only)"""
        # Save state when app goes to background
        self.logger.info("Application paused")
        return True

    def on_resume(self):
        """Resume the application (mobile only)"""
        self.logger.info("Application resumed")

    def on_stop(self):
        """Clean up when application stops"""
        try:
            # Save any ongoing session
            if self.current_session and not self.current_session.is_completed:
                self.current_session.end_session()

            # Close database
            self.db.close()

            # Save configuration
            self.config.save_config()

            self.logger.info("Application stopped cleanly")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

        return True

def main():
    """Main entry point"""
    try:
        app = LineUpProApp()
        return app.run()
    except Exception as e:
        # Basic error handling for startup failures
        error_log = Path('startup_error.log')
        with open(error_log, 'w') as f:
            f.write(f"Startup error: {str(e)}\n")
            import traceback
            traceback.print_exc(file=f)

        print(f"Application failed to start. Check {error_log} for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
