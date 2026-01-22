from kivy.app import App
from kivy.properties import StringProperty

# Try to import KivyMD widgets
try:
    from kivymd.uix.label import MDLabel as BaseLabel
    from kivymd.uix.button import MDRaisedButton as BaseButton
    USING_KIVYMD = True
except ImportError:
    from kivy.uix.label import Label as BaseLabel
    from kivy.uix.button import Button as BaseButton
    USING_KIVYMD = False


class TranslatableMixin:
    """Mixin for widgets that need translation support"""
    
    def translate(self, key, **kwargs):
        """Translate a key using the app's translation system"""
        app = App.get_running_app()
        if app and hasattr(app, 'translate'):
            return app.translate(key, **kwargs)
        return key
    
    def update_translation(self, *args):
        """Update widget text based on translation_key"""
        if hasattr(self, 'translation_key') and self.translation_key:
            if hasattr(self, 'text'):
                self.text = self.translate(self.translation_key)


class TranslatableLabel(BaseLabel, TranslatableMixin):
    """Label with automatic translation support"""
    translation_key = StringProperty('')
    
    def __init__(self, **kwargs):
        # Handle KivyMD specific properties
        if not USING_KIVYMD and 'font_style' in kwargs:
            kwargs.pop('font_style', None)
        
        super().__init__(**kwargs)
        TranslatableMixin.__init__(self)
        
        self.bind(translation_key=self.update_translation)
        # Initial update
        if self.translation_key:
            self.update_translation()


class TranslatableButton(BaseButton, TranslatableMixin):
    """Button with automatic translation support"""
    translation_key = StringProperty('')
    
    def __init__(self, **kwargs):
        # Handle KivyMD specific properties
        if not USING_KIVYMD and 'md_bg_color' in kwargs:
            kwargs.pop('md_bg_color', None)
        
        super().__init__(**kwargs)
        TranslatableMixin.__init__(self)
        
        self.bind(translation_key=self.update_translation)
        # Initial update
        if self.translation_key:
            self.update_translation()
