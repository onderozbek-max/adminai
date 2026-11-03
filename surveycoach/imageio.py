"""Facts about an image file, measured with Pillow only."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter

BLUR_MIN = 40          # edge strength below this reads as blurry; a starting value to calibrate on real surveys
ANALYSIS_WIDTH = 800   # resize first so scores are comparable across image sizes
EDGE_PERCENTILE = 0.99


@dataclass(frozen=True)
class ImageFacts:
    width: int
    height: int
    bytes: int
    format: str
    has_alpha: bool
    blur_score: float


def _edge_strength(image: Image.Image) -> float:
    """99th percentile of edge strength. Robust for clean product shots on white: sharp edges
    still produce strong responses even when most of the frame is flat."""
    gray = image.convert("L")
    if gray.width > ANALYSIS_WIDTH:
        gray = gray.resize((ANALYSIS_WIDTH, round(gray.height * ANALYSIS_WIDTH / gray.width)))
    histogram = gray.filter(ImageFilter.FIND_EDGES).histogram()
    target, seen = sum(histogram) * EDGE_PERCENTILE, 0
    for value, count in enumerate(histogram):
        seen += count
        if seen >= target:
            return float(value)
    return 255.0


def analyze_image(path: str | Path) -> ImageFacts:
    path = Path(path)
    with Image.open(path) as image:
        has_alpha = image.mode in {"RGBA", "LA", "PA"} or "transparency" in image.info
        return ImageFacts(width=image.width, height=image.height, bytes=path.stat().st_size,
                          format=image.format or "", has_alpha=has_alpha, blur_score=_edge_strength(image))
