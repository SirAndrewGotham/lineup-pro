from kivy.properties import StringProperty, ListProperty
from kivy.event import EventDispatcher
from kivy.clock import Clock

from utils.translation import translation_manager

class TranslatableMixin(EventDispatcher):
    """Mixin for Kivy widgets that need translation support"""

    # Properties that Kivy will watch
    translation_key = StringProperty('')
    translation_args = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(translation_key=self._update_translation)
        self.bind(translation_args=self._update_translation)

        # Schedule initial update
        Clock.schedule_once(lambda dt: self._update_translation(), 0)

    def _update_translation(self, *args):
        """Update widget text based on translation key"""
        if hasattr(self, 'text') and self.translation_key:
            try:
                if self.translation_args:
                    self.text = translation_manager.translate(
                        self.translation_key,
                        *self.translation_args
                    )
                else:
                    self.text = translation_manager.translate(self.translation_key)
            except Exception as e:
                print(f"Translation error for key '{self.translation_key}': {e}")

    def set_translation(self, key: str, **kwargs):
        """Convenience method to set translation"""
        self.translation_key = key
        if kwargs:
            self.translation_args = list(kwargs.values())
