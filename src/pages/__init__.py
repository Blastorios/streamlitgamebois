from .youtube import YouTubeDownloader
from .molstar import MolStar
from .test_page import Testing
from utils import Page

from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    "YouTube Downloader": YouTubeDownloader,
    # "Testing": Testing,
    "MolStar": MolStar,
}

__all__ = ["PAGE_MAP"]
