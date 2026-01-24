# ui/screens/settings_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Import our translatable widgets
from utils.translation_mixin import TranslatableLabel, TranslatableButton


class SettingsScreen(Screen):
    """Settings screen for the application"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        self.setup_ui()

    def setup_ui(self):
        # Create main layout
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(1, 1)
        )

        # Title - Remove font_style if not using KivyMD
        title = TranslatableLabel(
            translation_key='settings_title',
            font_size='24sp',
            size_hint=(1, 0.2),
            halign='center'
        )
        layout.add_widget(title)

        # Language section
        lang_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            spacing=10
        )

        lang_label = TranslatableLabel(
            translation_key='language_label',
            size_hint=(0.4, 1),
            halign='right'
        )

        from kivy.uix.button import Button
        self.lang_button = Button(
            text='English',
            size_hint=(0.6, 1)
        )
        self.lang_button.bind(on_release=self.toggle_language)

        lang_layout.add_widget(lang_label)
        lang_layout.add_widget(self.lang_button)
        layout.add_widget(lang_layout)

        # Back button
        back_btn = TranslatableButton(
            translation_key='back_button',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1) if hasattr(TranslatableButton, 'background_color') else None
        )
        back_btn.bind(on_release=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

        # Update language button text
        self.update_language_button()

    def toggle_language(self, instance):
        """Toggle between Russian and English"""
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        if app and hasattr(app, 'config_manager'):
            # Get current language
            current_lang = app.config_manager.get('ui.language', 'ru')
            new_lang = 'en' if current_lang == 'ru' else 'ru'

            # Save the new language setting
            app.config_manager.set('ui.language', new_lang)

            # Update translation manager
            if hasattr(app, 'translation_manager'):
                app.translation_manager.set_language(new_lang)

            # Update button text
            instance.text = 'English' if new_lang == 'ru' else 'Русский'

            # Update all screens
            self.update_all_translations()

    def update_all_translations(self):
        """Update translations on all screens"""
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        if app and hasattr(app, 'sm'):
            # Update each screen that has an update_translations method
            for screen_name in app.sm.screen_names:
                screen = app.sm.get_screen(screen_name)
                if hasattr(screen, 'update_translations'):
                    screen.update_translations()

    def update_language_button(self):
        """Update the language button text"""
        from kivy.app import App
        app = App.get_running_app()

        if hasattr(app, 'config_manager'):
            current_lang = app.config_manager.get("general", "language") or "en"
            self.lang_button.text = 'Русский' if current_lang == 'en' else 'English'

    def go_back(self, instance):
        """Return to main menu"""
        self.manager.current = 'main'
