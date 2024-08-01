# bookmark_parser/__init__.py

from .parser import BookmarkParser, Folder
from .utils import netscape  

# Package information
__version__ = "0.1.0"
__all__ = ["BookmarkParser", "Folder", "netscape"]