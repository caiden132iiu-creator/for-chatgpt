"""Shared output location; works both in the workspace and the extracted archive."""
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
DEFAULT_ROOT=HERE.parent if (HERE.parent/'original_wishlist.txt').is_file() else HERE.parent/'html-wishlist-1500'
ROOT=Path(os.environ.get('HTML_WISHLIST_OUTPUT',str(DEFAULT_ROOT))).resolve()
