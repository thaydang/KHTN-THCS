"""LaTeX formula rendering utility using Matplotlib.

This module provides functions to render LaTeX mathematical expressions
as images (PNG format) that can be embedded in PDF and Word documents.
"""

from __future__ import annotations

import hashlib
import io
from pathlib import Path
from typing import Dict, Optional

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import mathtext
from PIL import Image

# Use Agg backend for non-interactive rendering
matplotlib.use("Agg")


class LatexRenderer:
    """Renders LaTeX formulas to images using Matplotlib."""

    def __init__(self, output_dir: Optional[Path] = None, dpi: int = 300, max_cache_size: int = 128):
        """Initialize the LaTeX renderer.

        Args:
            output_dir: Directory to save rendered images. If None, uses 'outputs/formulas'
            dpi: Resolution of the output images (default: 300 for high quality)
            max_cache_size: Maximum number of formulas to cache in memory (default: 128)
        """
        self.output_dir = output_dir or Path("outputs/formulas")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
        self.max_cache_size = max_cache_size
        # Cache for in-memory byte rendering to avoid re-rendering same formulas
        # Uses LRU eviction when cache exceeds max_cache_size
        self._bytes_cache: Dict[str, bytes] = {}
        self._cache_access_order: list = []  # Track access order for LRU eviction

    def _generate_filename(self, latex_expr: str) -> str:
        """Generate a unique filename for a LaTeX expression.

        Args:
            latex_expr: LaTeX expression string

        Returns:
            Filename with .png extension
        """
        # Use hash to create unique but consistent filenames
        hash_obj = hashlib.md5(latex_expr.encode("utf-8"))
        return f"formula_{hash_obj.hexdigest()[:12]}.png"

    def render_to_file(
        self, latex_expr: str, output_path: Optional[Path] = None
    ) -> Path:
        """Render a LaTeX expression to a PNG file.

        Args:
            latex_expr: LaTeX expression (e.g., "F = ma" or "\\frac{a}{b}")
            output_path: Path to save the image. If None, generates a unique filename.

        Returns:
            Path to the saved image file

        Raises:
            ValueError: If LaTeX expression is invalid or cannot be rendered
        """
        if not latex_expr or not latex_expr.strip():
            raise ValueError("LaTeX expression cannot be empty")

        # Clean the expression (remove surrounding $ if present)
        latex_expr = latex_expr.strip()
        if latex_expr.startswith("$") and latex_expr.endswith("$"):
            latex_expr = latex_expr[1:-1].strip()

        if output_path is None:
            filename = self._generate_filename(latex_expr)
            output_path = self.output_dir / filename

        # Check if file already exists to avoid re-rendering
        if output_path.exists():
            return output_path

        try:
            # Create a figure with transparent background
            fig = plt.figure(figsize=(10, 2))
            fig.patch.set_alpha(0.0)

            # Render the LaTeX expression
            # Use displaystyle for better formatting of fractions, etc.
            text = fig.text(
                0.5,
                0.5,
                f"${latex_expr}$",
                fontsize=20,
                ha="center",
                va="center",
                usetex=False,  # Use matplotlib's built-in LaTeX parser
            )

            # Get the bounding box and save with tight layout
            fig.savefig(
                output_path,
                dpi=self.dpi,
                bbox_inches="tight",
                pad_inches=0.1,
                transparent=True,
                format="png",
            )
            plt.close(fig)

            return output_path

        except Exception as e:
            raise ValueError(f"Failed to render LaTeX expression: {e}") from e

    def render_to_bytes(self, latex_expr: str) -> bytes:
        """Render a LaTeX expression to PNG bytes in memory.

        Uses bounded LRU caching to avoid re-rendering the same formula multiple times,
        while preventing unbounded memory growth in long-running applications.

        Args:
            latex_expr: LaTeX expression

        Returns:
            PNG image data as bytes

        Raises:
            ValueError: If LaTeX expression is invalid or cannot be rendered
        """
        if not latex_expr or not latex_expr.strip():
            raise ValueError("LaTeX expression cannot be empty")

        # Clean the expression
        latex_expr = latex_expr.strip()
        if latex_expr.startswith("$") and latex_expr.endswith("$"):
            latex_expr = latex_expr[1:-1].strip()

        # Check cache first
        cache_key = f"{latex_expr}:{self.dpi}"
        if cache_key in self._bytes_cache:
            # Update LRU order: move to end (most recently used)
            self._cache_access_order.remove(cache_key)
            self._cache_access_order.append(cache_key)
            return self._bytes_cache[cache_key]

        try:
            fig = plt.figure(figsize=(10, 2))
            fig.patch.set_alpha(0.0)

            text = fig.text(
                0.5,
                0.5,
                f"${latex_expr}$",
                fontsize=20,
                ha="center",
                va="center",
                usetex=False,
            )

            # Save to bytes buffer
            buf = io.BytesIO()
            fig.savefig(
                buf,
                dpi=self.dpi,
                bbox_inches="tight",
                pad_inches=0.1,
                transparent=True,
                format="png",
            )
            plt.close(fig)

            buf.seek(0)
            result = buf.getvalue()
            
            # Evict least recently used item if cache is full
            if len(self._bytes_cache) >= self.max_cache_size:
                lru_key = self._cache_access_order.pop(0)
                del self._bytes_cache[lru_key]
            
            # Cache the result
            self._bytes_cache[cache_key] = result
            self._cache_access_order.append(cache_key)
            return result

        except Exception as e:
            raise ValueError(f"Failed to render LaTeX expression: {e}") from e


def render_latex_to_file(
    latex_expr: str, output_path: Path, dpi: int = 300
) -> Path:
    """Convenience function to render a single LaTeX expression to a file.

    Args:
        latex_expr: LaTeX expression to render
        output_path: Path where the image should be saved
        dpi: Resolution of the output image

    Returns:
        Path to the saved image file
    """
    renderer = LatexRenderer(output_dir=output_path.parent, dpi=dpi)
    return renderer.render_to_file(latex_expr, output_path)


def render_latex_to_bytes(latex_expr: str, dpi: int = 300) -> bytes:
    """Convenience function to render a single LaTeX expression to bytes.

    Args:
        latex_expr: LaTeX expression to render
        dpi: Resolution of the output image

    Returns:
        PNG image data as bytes
    """
    renderer = LatexRenderer(dpi=dpi)
    return renderer.render_to_bytes(latex_expr)
