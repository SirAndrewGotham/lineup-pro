# ui/screens/main_screen.py - Fixed version with better styling
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from utils.translation_mixin import TranslatableLabel, TranslatableButton


class MainScreen(Screen):
    """Main menu screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.setup_ui()

    def setup_ui(self):
        # Get app instance for translation
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        # Create main layout with background color
        layout = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            size_hint=(1, 1)
        )

        # Set background color for the entire screen
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Logo - Check if file exists with fallback
        logo_path = 'assets/images/logo.png'
        placeholder_path = 'assets/images/placeholder.png'

        # Choose image source
        if os.path.exists(logo_path):
            image_source = logo_path
        elif os.path.exists(placeholder_path):
            image_source = placeholder_path
        else:
            image_source = None

        if image_source:
            logo = Image(
                source=image_source,
                size_hint=(1, 0.4),
                allow_stretch=True,
                keep_ratio=True
            )
            layout.add_widget(logo)
        else:
            # If no images exist, show title
            title = TranslatableLabel(
                translation_key='main.title',
                font_size='32sp',
                halign='center',
                size_hint=(1, 0.2),
                color=(0.2, 0.2, 0.2, 1),  # Dark gray text
                bold=True
            )
            layout.add_widget(title)

        # Subtitle
        subtitle = TranslatableLabel(
            translation_key='main.subtitle',
            font_size='18sp',
            halign='center',
            size_hint=(1, 0.1),
            color=(0.4, 0.4, 0.4, 1)  # Medium gray text
        )
        layout.add_widget(subtitle)

        # Create buttons for different modes with better styling
        buttons = [
            ('main.training_mode', self.start_training, (0.2, 0.6, 0.8, 1)),  # Blue
            ('main.practice_mode', self.start_practice, (0.3, 0.7, 0.5, 1)),  # Green
            ('main.exam_mode', self.start_exam, (0.8, 0.4, 0.2, 1)),  # Orange
            ('main.flashcards_mode', self.start_flashcards, (0.7, 0.3, 0.8, 1)),  # Purple
            ('main.progress_tracking', self.show_progress, (0.4, 0.5, 0.9, 1)),  # Blue-purple
            ('main.settings', self.show_settings, (0.5, 0.5, 0.5, 1)),  # Gray
            ('main.exit', self.exit_app, (0.8, 0.2, 0.2, 1))  # Red
        ]

        for translation_key, callback, color in buttons:
            btn = TranslatableButton(
                translation_key=translation_key,
                size_hint=(1, 0.12),
                background_color=color,
                background_normal='',  # Remove default button image
                background_down='',  # Remove pressed state image
                color=(1, 1, 1, 1),  # White text
                font_size='18sp',
                bold=True
            )
            btn.bind(on_release=callback)
            layout.add_widget(btn)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        """Update background rectangle size and position"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

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

    def start_flashcards(self, instance):
        """Start flashcards mode"""
        print("Starting flashcards mode")
        self.manager.current = 'flashcards'

    def on_enter(self, *args):
        """Called when screen becomes active - update translations"""
        self.update_translations()

    def update_translations(self):
        """Update all translatable widgets on this screen"""
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        if app and hasattr(app, 'translation_manager'):
            for child in self.walk():
                if hasattr(child, 'translation_key') and child.translation_key:
                    translated_text = app.translation_manager.translate(child.translation_key)
                    if hasattr(child, 'text'):
                        child.text = translated_text
