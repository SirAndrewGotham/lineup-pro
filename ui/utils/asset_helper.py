# ui/utils/asset_helper.py
import os
from pathlib import Path

class AssetHelper:
    """Helper for managing assets with fallbacks"""

    @staticmethod
    def get_image(path: str, fallback_to_placeholder=True) -> str:
        """Get image path with placeholder fallback"""
        assets_root = Path(__file__).parent.parent.parent / 'assets'
        full_path = assets_root / path

        if full_path.exists():
            return str(full_path)

        if fallback_to_placeholder:
            placeholder = assets_root / 'images' / 'placeholder.png'
            if placeholder.exists():
                return str(placeholder)

        return ''

    @staticmethod
    def asset_exists(path: str) -> bool:
        """Check if asset exists"""
        assets_root = Path(__file__).parent.parent.parent / 'assets'
        return (assets_root / path).exists()
