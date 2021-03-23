from .youtube import YouTubeDownloader
from .test_page import Testing
from utils import Page

from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    "YouTubeDownloader": YouTubeDownloader,
    # "Testing": Testing,
    # "Page 2": Page2,
}

__all__ = ["PAGE_MAP"]
