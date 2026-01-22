# ui/screens/main_screen.py - Fixed version
import os
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from utils.translation_mixin import TranslatableLabel, TranslatableButton, TranslatableMixin


class MainScreen(Screen, TranslatableMixin):
    """Main menu screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.setup_ui()

    def setup_ui(self):
        # Create main layout
        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            size_hint=(1, 1)
        )

        # Logo - Check if file exists
        logo_path = 'assets/images/logo.png'
        if os.path.exists(logo_path):
            logo = Image(
                source=logo_path,
                size_hint=(1, 0.4),
                allow_stretch=True,
                keep_ratio=True
            )
            layout.add_widget(logo)
        else:
            # If no logo, add a title instead
            title = TranslatableLabel(
                translation_key='app_title',
                font_style='H3',
                halign='center',
                size_hint=(1, 0.2)
            )
            layout.add_widget(title)

        # Subtitle
        subtitle = TranslatableLabel(
            translation_key='main_title',
            font_style='H5',
            halign='center',
            size_hint=(1, 0.1)
        )
        layout.add_widget(subtitle)

        # Create buttons for different modes
        buttons = [
            ('training_button', self.start_training),
            ('practice_button', self.start_practice),
            ('exam_button', self.start_exam),
            ('progress_button', self.show_progress),
            ('settings_button', self.show_settings),
            ('exit_button', self.exit_app)
        ]

        for translation_key, callback in buttons:
            btn = TranslatableButton(
                translation_key=translation_key,
                size_hint=(1, 0.12),
                md_bg_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_release=callback)
            layout.add_widget(btn)

        self.add_widget(layout)

    def start_training(self, instance):
        """Start guided training mode"""
        print("Starting training mode")
        # self.manager.current = 'training'

    def start_practice(self, instance):
        """Start practice mode"""
        print("Starting practice mode")
        # self.manager.current = 'practice'

    def start_exam(self, instance):
        """Start exam mode"""
        print("Starting exam mode")
        # self.manager.current = 'exam'

    def show_progress(self, instance):
        """Show progress screen"""
        print("Showing progress")
        # self.manager.current = 'progress'

    def show_settings(self, instance):
        """Show settings screen"""
        print("Showing settings")
        self.manager.current = 'settings'

    def exit_app(self, instance):
        """Exit the application"""
        from kivy.app import App
        App.get_running_app().stop()
