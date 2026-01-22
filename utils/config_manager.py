import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from utils.translation import translation_manager
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_default_config()
        self.load_config()

        # If config doesn't exist but template does, copy it
        if not self.config_path.exists() and self.template_path.exists():
            self._create_from_template()

        self.load_config()

        # Set language from config
        self._apply_language()

    def _apply_language(self):
        """Apply language setting from config"""
        lang = self.get('ui.language', 'ru')  # Default to Russian
        translation_manager.set_language(lang)

    def _create_from_template(self):
        """Create user config from template"""
        try:
            import shutil
            shutil.copy(self.template_path, self.config_path)
            logger.info(f"Created config from template: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to create config from template: {e}")

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "app": {
                "name": "LineUp Pro",
                "version": "1.0.0",
                "developer_mode": False
            },
            "training": {
                "default_mode": "guided",
                "show_timer": True,
                "enable_sounds": True,
                "enable_haptics": False,
                "voice_guidance": False,
                "auto_advance": True
            },
            "scoring": {
                "passing_score": 70,
                "time_bonus_enabled": True,
                "show_detailed_feedback": True
            },
            "ui": {
                "theme": "light",
                "language": "ru",
                "font_size": "medium",
                "animation_speed": "normal"
            },
            "data": {
                "auto_backup": True,
                "backup_interval_hours": 24,
                "sync_enabled": False,
                "sync_server_url": ""
            },
            "paths": {
                "assets": "assets/",
                "database": "lineup_pro.db",
                "backups": "backups/",
                "exports": "exports/"
            }
        }

    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self._merge_configs(loaded_config)
                logger.info(f"Configuration loaded from {self.config_path}")
                return True
            else:
                self.save_config()  # Create default config file
                return True
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False

    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def _merge_configs(self, new_config: Dict[str, Any]):
        """Merge loaded config with defaults"""
        def merge_dicts(dict1, dict2):
            for key, value in dict2.items():
                if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                    merge_dicts(dict1[key], value)
                else:
                    dict1[key] = value

        merge_dicts(self.config, new_config)

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation path"""
        keys = key_path.split('.')
        value = self.config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any) -> bool:
        """Set configuration value by dot-notation path"""
        keys = key_path.split('.')
        config_ref = self.config

        try:
            # Navigate to the parent of the final key
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]

            # Set the final value
            config_ref[keys[-1]] = value

            # If language changed, update translation manager
            if key_path == 'ui.language':
                translation_manager.set_language(value)

            # Save automatically
            self.save_config()
            return True
        except Exception as e:
            logger.error(f"Error setting configuration {key_path}: {e}")
            return False

    # Method to get language display names
    def get_language_options(self) -> Dict[str, str]:
        """Get available languages with display names"""
        return translation_manager.get_available_languages()

    def get_training_settings(self) -> Dict[str, Any]:
        """Get training-specific settings"""
        return self.config.get('training', {})

    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI-specific settings"""
        return self.config.get('ui', {})

    def toggle_developer_mode(self):
        """Toggle developer mode"""
        current = self.get('app.developer_mode', False)
        self.set('app.developer_mode', not current)

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self._load_default_config()
        self.save_config()
        logger.info("Configuration reset to defaults")
