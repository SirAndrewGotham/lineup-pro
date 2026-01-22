# utils/translation_mixin.py
from kivy.app import App
from kivy.properties import StringProperty


class TranslationMixin:
    """Mixin class for widgets that need translation support"""

    def translate(self, key, **kwargs):
        """Translate a key using the app's translation system"""
        app = App.get_running_app()
        if app and hasattr(app, 'translate'):
            return app.translate(key, **kwargs)
        return key


# Try to import KivyMD widgets, fallback to regular Kivy
try:
    from kivymd.uix.label import MDLabel
    from kivymd.uix.button import MDRaisedButton
    KIVYMD_AVAILABLE = True
except ImportError:
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    KIVYMD_AVAILABLE = False

    # Define aliases for consistency
    MDLabel = Label
    MDRaisedButton = Button


class TranslatableLabel(MDLabel):
    """Label that automatically updates its text based on current language"""
    translation_key = StringProperty('')

    def __init__(self, **kwargs):
        # Remove font_style if it's passed and we're not using KivyMD
        if not KIVYMD_AVAILABLE and 'font_style' in kwargs:
            kwargs.pop('font_style')

        super().__init__(**kwargs)
        self.bind(translation_key=self._update_text)

        # Initial update if translation_key is set
        if self.translation_key:
            self._update_text(None, self.translation_key)

    def _update_text(self, instance, value):
        if value:
            app = App.get_running_app()
            if app and hasattr(app, 'translate'):
                self.text = app.translate(value)


class TranslatableButton(MDRaisedButton):
    """Button that automatically updates its text based on current language"""
    translation_key = StringProperty('')

    def __init__(self, **kwargs):
        # Remove md_bg_color if it's passed and we're not using KivyMD
        if not KIVYMD_AVAILABLE and 'md_bg_color' in kwargs:
            kwargs.pop('md_bg_color')

        super().__init__(**kwargs)
        self.bind(translation_key=self._update_text)

        # Initial update if translation_key is set
        if self.translation_key:
            self._update_text(None, self.translation_key)

    def _update_text(self, instance, value):
        if value:
            app = App.get_running_app()
            if app and hasattr(app, 'translate'):
                self.text = app.translate(value)
