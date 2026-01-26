"""Tests for LaTeX rendering functionality."""

import unittest
from pathlib import Path
import tempfile
import shutil

from app.latex_renderer import LatexRenderer, render_latex_to_file, render_latex_to_bytes


class LatexRendererTests(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for test outputs."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_render_simple_formula(self):
        """Test rendering a simple formula."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = "F = ma"

        output_path = renderer.render_to_file(latex_expr)

        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.suffix, ".png")
        self.assertGreater(output_path.stat().st_size, 0)

    def test_render_fraction(self):
        """Test rendering a fraction formula."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = r"\dfrac{P}{4\pi r^2}"

        output_path = renderer.render_to_file(latex_expr)

        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_render_with_dollar_signs(self):
        """Test that dollar signs are properly stripped."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = "$E = mc^2$"

        output_path = renderer.render_to_file(latex_expr)

        self.assertTrue(output_path.exists())

    def test_render_empty_expression_raises_error(self):
        """Test that empty expression raises ValueError."""
        renderer = LatexRenderer(output_dir=self.test_dir)

        with self.assertRaises(ValueError):
            renderer.render_to_file("")

        with self.assertRaises(ValueError):
            renderer.render_to_file("   ")

    def test_render_to_bytes(self):
        """Test rendering to bytes."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = "a^2 + b^2 = c^2"

        image_bytes = renderer.render_to_bytes(latex_expr)

        self.assertIsInstance(image_bytes, bytes)
        self.assertGreater(len(image_bytes), 0)
        # PNG files start with specific magic bytes
        self.assertTrue(image_bytes.startswith(b"\x89PNG"))

    def test_caching_same_formula(self):
        """Test that the same formula is cached."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = "v = v_0 + at"

        # First render
        path1 = renderer.render_to_file(latex_expr)
        mtime1 = path1.stat().st_mtime

        # Second render of same formula
        path2 = renderer.render_to_file(latex_expr)
        mtime2 = path2.stat().st_mtime

        # Should be the same file (cached)
        self.assertEqual(path1, path2)
        self.assertEqual(mtime1, mtime2)

    def test_render_to_bytes_caching(self):
        """Test that render_to_bytes() caches results in memory."""
        renderer = LatexRenderer(output_dir=self.test_dir)
        latex_expr = "E = mc^2"

        # First render
        bytes1 = renderer.render_to_bytes(latex_expr)
        
        # Second render of same formula
        bytes2 = renderer.render_to_bytes(latex_expr)

        # Should be the same cached object (same identity)
        self.assertIs(bytes1, bytes2, "render_to_bytes() should return cached result")
        
        # Verify it's valid PNG data
        self.assertTrue(bytes1.startswith(b"\x89PNG"))

    def test_render_to_bytes_caching_different_dpi(self):
        """Test that cache considers DPI in the cache key."""
        renderer1 = LatexRenderer(output_dir=self.test_dir, dpi=150)
        renderer2 = LatexRenderer(output_dir=self.test_dir, dpi=300)
        latex_expr = "a + b = c"

        # Render with different DPI
        bytes1 = renderer1.render_to_bytes(latex_expr)
        bytes2 = renderer2.render_to_bytes(latex_expr)

        # Should be different objects (different DPI)
        self.assertIsNot(bytes1, bytes2, "Different DPI should produce different cached results")
        
        # But both should be valid
        self.assertTrue(bytes1.startswith(b"\x89PNG"))
        self.assertTrue(bytes2.startswith(b"\x89PNG"))

    def test_convenience_functions(self):
        """Test convenience functions."""
        latex_expr = r"\nabla n = \frac{\Delta n}{\Delta x}"

        # Test file rendering
        output_path = self.test_dir / "test_formula.png"
        result_path = render_latex_to_file(latex_expr, output_path)
        self.assertEqual(output_path, result_path)
        self.assertTrue(output_path.exists())

        # Test bytes rendering
        image_bytes = render_latex_to_bytes(latex_expr)
        self.assertIsInstance(image_bytes, bytes)
        self.assertGreater(len(image_bytes), 0)


if __name__ == "__main__":
    unittest.main()
