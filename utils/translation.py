import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TranslationManager:
    """Manages application translations"""

    def __init__(self, locales_dir: str = "assets/locales"):
        self.locales_dir = Path(locales_dir)
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.current_language = "ru"  # Default to Russian
        self.fallback_language = "en"

        self.load_all_translations()

    def load_all_translations(self):
        """Load all available translation files"""
        if not self.locales_dir.exists():
            logger.error(f"Locales directory not found: {self.locales_dir}")
            return

        for lang_file in self.locales_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
                logger.info(f"Loaded translations for language: {lang_code}")
            except Exception as e:
                logger.error(f"Failed to load translations for {lang_code}: {e}")

    def set_language(self, lang_code: str):
        """Set current language"""
        if lang_code in self.translations:
            self.current_language = lang_code
            logger.info(f"Language set to: {lang_code}")
            return True
        else:
            logger.warning(f"Language not available: {lang_code}")
            return False

    def get_available_languages(self) -> Dict[str, str]:
        """Get dictionary of available languages with their display names"""
        languages = {}
        for lang_code, translations in self.translations.items():
            display_name = translations.get('settings', {}).get('language_options', {}).get(lang_code, lang_code.upper())
            languages[lang_code] = display_name
        return languages

    def translate(self, key: str, **kwargs) -> str:
        """Get translation for a key, with fallback support"""
        # Split key by dots to navigate nested structure
        keys = key.split('.')

        # Try current language first
        translation = self._get_nested_translation(self.current_language, keys)

        # Fallback to English if not found
        if translation is None and self.current_language != self.fallback_language:
            translation = self._get_nested_translation(self.fallback_language, keys)

        # If still not found, return the key itself
        if translation is None:
            logger.warning(f"Translation key not found: {key}")
            return key

        # Format with kwargs if provided
        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation

        return translation

    def _get_nested_translation(self, lang_code: str, keys: list) -> str:
        """Get translation from nested dictionary structure"""
        if lang_code not in self.translations:
            return None

        current = self.translations[lang_code]
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None

        return str(current) if not isinstance(current, dict) else None

    def get_all(self, prefix: str = "") -> Dict[str, str]:
        """Get all translations for a specific prefix"""
        result = {}
        keys_to_find = prefix.split('.') if prefix else []

        def _collect_translations(data, current_keys):
            for key, value in data.items():
                full_key = '.'.join(current_keys + [key]) if current_keys else key
                if isinstance(value, dict):
                    _collect_translations(value, current_keys + [key])
                else:
                    result[full_key] = str(value)

        # Collect from current language
        if self.current_language in self.translations:
            target_data = self.translations[self.current_language]
            for k in keys_to_find:
                if isinstance(target_data, dict) and k in target_data:
                    target_data = target_data[k]
                else:
                    return {}

            _collect_translations(target_data, keys_to_find)

        return result

# Global instance
translation_manager = TranslationManager()
