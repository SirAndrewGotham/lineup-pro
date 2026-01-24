"""
Translation mixin for Kivy widgets to support multilingual text.
"""
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

# REMOVE THIS LINE - it's causing circular imports
# from utils.translation import TranslationManager


class TranslationMixin(EventDispatcher):
    """Mixin class to add translation support to Kivy widgets"""

    translation_key = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(translation_key=self.on_translation_key)

    def on_translation_key(self, instance, value):
        """Called when translation_key changes"""
        if value:
            self.setup_translation()

    def setup_translation(self):
        """Setup translation for this widget"""
        # Get translation manager
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        if app and hasattr(app, 'translation_manager'):
            # Store reference to app for updates
            self.app = app
            # Set initial translation
            self.update_translation()

    def update_translation(self, *args):
        """Update widget text with current translation"""
        if hasattr(self, 'app') and self.app and hasattr(self.app, 'translation_manager') and self.translation_key:
            translated_text = self.app.translation_manager.translate(self.translation_key)
            if hasattr(self, 'text'):
                self.text = translated_text


class TranslatableLabel(Label, TranslationMixin):
    """Label widget with translation support"""

    def __init__(self, **kwargs):
        # Store translation key if provided
        self.translation_key = kwargs.pop('translation_key', None)

        # Call parent constructors
        super().__init__(**kwargs)

        # Set up translation
        if self.translation_key:
            self.setup_translation()


class TranslatableButton(Button, TranslationMixin):
    """Button widget with translation support"""

    def __init__(self, **kwargs):
        # Store translation key if provided
        self.translation_key = kwargs.pop('translation_key', None)

        # Call parent constructors
        super().__init__(**kwargs)

        # Set up translation
        if self.translation_key:
            self.setup_translation()
