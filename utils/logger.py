import logging
import sys
from pathlib import Path

def setup_logging():
    """Setup application logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "lineup_pro.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce Kivy log noise
    logging.getLogger('kivy').setLevel(logging.WARNING)
