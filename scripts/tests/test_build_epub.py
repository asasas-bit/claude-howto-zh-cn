"""Tests for the EPUB builder module."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from bs4 import BeautifulSoup
from ebooklib import epub

# Fixtures are imported from conftest.py automatically by pytest
# Import from parent directory (handled by conftest.py sys.path)
from build_epub import (
    BuildState,
    ChapterCollector,
    EPUBConfig,
    MermaidRenderer,
    MermaidRenderError,
    ValidationError,
    create_chapter_html,
    create_cover_image,
    embed_local_raster_images,
    extract_all_mermaid_blocks,
    extract_markdown_h1,
    get_chapter_order,
    prepare_root_readme_for_epub,
    process_mermaid_blocks,
    sanitize_mermaid,
    setup_logging,
    validate_inputs,
)

# =============================================================================
# BuildState Tests
# =============================================================================


class TestBuildState:
    """Tests for BuildState dataclass."""

    def test_initial_state(self, state: BuildState) -> None:
        """Test that initial state is empty."""
        assert state.mermaid_counter == 0
        assert len(state.mermaid_cache) == 0
        assert len(state.mermaid_added_to_book) == 0
        assert len(state.embedded_assets) == 0
        assert len(state.path_to_chapter) == 0

    def test_state_modification(self, state: BuildState) -> None:
        """Test that state can be modified."""
        state.mermaid_counter = 5
        state.mermaid_cache["key"] = (b"data", "file.png")
        state.mermaid_added_to_book.add("file.png")
        state.embedded_assets.add("logo.png")
        state.path_to_chapter["README.md"] = "chap_01.xhtml"

        assert state.mermaid_counter == 5
        assert state.mermaid_cache["key"] == (b"data", "file.png")
        assert "file.png" in state.mermaid_added_to_book
        assert "logo.png" in state.embedded_assets
        assert state.path_to_chapter["README.md"] == "chap_01.xhtml"

    def test_reset(self, state: BuildState) -> None:
        """Test that reset clears all state."""
        state.mermaid_counter = 5
        state.mermaid_cache["key"] = (b"data", "file.png")
        state.mermaid_added_to_book.add("file.png")
        state.embedded_assets.add("logo.png")
        state.path_to_chapter["README.md"] = "chap_01.xhtml"

        state.reset()

        assert state.mermaid_counter == 0
        assert len(state.mermaid_cache) == 0
        assert len(state.mermaid_added_to_book) == 0
        assert len(state.embedded_assets) == 0
        assert len(state.path_to_chapter) == 0


# =============================================================================
# EPUBConfig Tests
# =============================================================================


class TestEPUBConfig:
    """Tests for EPUBConfig dataclass."""

    def test_required_fields(self, tmp_path: Path) -> None:
        """Test that required fields must be provided."""
        config = EPUBConfig(
            root_path=tmp_path,
            output_path=tmp_path / "out.epub",
        )
        assert config.root_path == tmp_path
        assert config.output_path == tmp_path / "out.epub"

    def test_default_values(self, tmp_path: Path) -> None:
        """Test that default values are set correctly."""
        config = EPUBConfig(
            root_path=tmp_path,
            output_path=tmp_path / "out.epub",
        )
        assert config.identifier == "claude-howto-zh-cn-guide"
        assert config.title == "Claude Code 中文全面上手指南"
        assert config.language == "zh"
        assert config.author == "claude-howto-zh-cn contributors"
        assert config.mmdc_path == "mmdc"
        assert config.puppeteer_config is None

    def test_custom_values(self, tmp_path: Path) -> None:
        """Test that custom values override defaults."""
        config = EPUBConfig(
            root_path=tmp_path,
            output_path=tmp_path / "out.epub",
            title="Custom Title",
            mmdc_path="/usr/local/bin/mmdc",
            puppeteer_config="puppeteer.json",
        )
        assert config.title == "Custom Title"
        assert config.mmdc_path == "/usr/local/bin/mmdc"
        assert config.puppeteer_config == "puppeteer.json"


# =============================================================================
# Validation Tests
# =============================================================================


class TestValidation:
    """Tests for input validation."""

    def test_valid_inputs(self, config: EPUBConfig, logger: logging.Logger) -> None:
        """Test that valid inputs pass validation."""
        # Should not raise
        validate_inputs(config, logger)

    def test_missing_root_path(self, tmp_path: Path, logger: logging.Logger) -> None:
        """Test that missing root path raises ValidationError."""
        config = EPUBConfig(
            root_path=tmp_path / "nonexistent",
            output_path=tmp_path / "out.epub",
        )
        with pytest.raises(ValidationError, match="Root path does not exist"):
            validate_inputs(config, logger)

    def test_root_path_is_file(self, tmp_path: Path, logger: logging.Logger) -> None:
        """Test that file as root path raises ValidationError."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        config = EPUBConfig(
            root_path=file_path,
            output_path=tmp_path / "out.epub",
        )
        with pytest.raises(ValidationError, match="Root path is not a directory"):
            validate_inputs(config, logger)

    def test_no_markdown_files(self, tmp_path: Path, logger: logging.Logger) -> None:
        """Test that directory with no markdown files raises ValidationError."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        config = EPUBConfig(
            root_path=empty_dir,
            output_path=tmp_path / "out.epub",
        )
        with pytest.raises(ValidationError, match="No markdown files found"):
            validate_inputs(config, logger)

    def test_missing_output_directory(
        self, tmp_project: Path, logger: logging.Logger
    ) -> None:
        """Test that missing output directory raises ValidationError."""
        config = EPUBConfig(
            root_path=tmp_project,
            output_path=tmp_project / "nonexistent" / "out.epub",
        )
        with pytest.raises(ValidationError, match="Output directory does not exist"):
            validate_inputs(config, logger)


class TestCoverGeneration:
    """Tests for cover image generation."""

    def test_create_cover_image_from_prebuilt_cover(
        self, tmp_path: Path, logger: logging.Logger
    ) -> None:
        cover_path = tmp_path / "cover.png"
        from PIL import Image as PILImage

        PILImage.new("RGB", (1200, 1800), color=(240, 240, 240)).save(cover_path, "PNG")

        config = EPUBConfig(
            root_path=tmp_path,
            output_path=tmp_path / "out.epub",
            cover_image_path=cover_path,
        )

        cover_bytes = create_cover_image(config, logger)

        assert len(cover_bytes) > 0


# =============================================================================
# Mermaid Processing Tests
# =============================================================================


class TestMermaidProcessing:
    """Tests for Mermaid diagram processing."""

    def test_sanitize_mermaid_numbered_list(self) -> None:
        """Test that numbered lists in brackets are escaped."""
        input_code = 'A["1. First item"] --> B["2. Second item"]'
        expected = 'A["1\\. First item"] --> B["2\\. Second item"]'
        assert sanitize_mermaid(input_code) == expected

    def test_sanitize_mermaid_no_change(self) -> None:
        """Test that code without numbered lists is unchanged."""
        input_code = "A --> B --> C"
        assert sanitize_mermaid(input_code) == input_code

    def test_extract_mermaid_blocks(
        self, tmp_path: Path, logger: logging.Logger
    ) -> None:
        """Test extraction of Mermaid blocks from files."""
        # Create test file with mermaid blocks
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """# Test

```mermaid
graph TD
    A --> B
```

Some text

```mermaid
graph LR
    C --> D
```
"""
        )

        diagrams = extract_all_mermaid_blocks([(md_file, "Test")], logger)

        assert len(diagrams) == 2
        assert diagrams[0][0] == 1  # First diagram index
        assert diagrams[1][0] == 2  # Second diagram index
        assert "A --> B" in diagrams[0][1]
        assert "C --> D" in diagrams[1][1]

    def test_extract_mermaid_blocks_deduplication(
        self, tmp_path: Path, logger: logging.Logger
    ) -> None:
        """Test that duplicate Mermaid blocks are deduplicated."""
        md_file1 = tmp_path / "test1.md"
        md_file2 = tmp_path / "test2.md"

        same_diagram = """```mermaid
graph TD
    A --> B
```"""

        md_file1.write_text(f"# File 1\n\n{same_diagram}")
        md_file2.write_text(f"# File 2\n\n{same_diagram}")

        diagrams = extract_all_mermaid_blocks(
            [(md_file1, "Test1"), (md_file2, "Test2")], logger
        )

        # Should only have one diagram since they're identical
        assert len(diagrams) == 1

    def test_mermaid_render_success(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """Local mmdc output is cached and returned as an EPUB image."""
        renderer = MermaidRenderer(config, state, logger)
        fake_png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32

        with (
            patch("shutil.which", return_value="/usr/bin/mmdc"),
            patch("subprocess.run") as run,
            patch("pathlib.Path.is_file", return_value=True),
            patch("pathlib.Path.read_bytes", return_value=fake_png),
        ):
            run.return_value = MagicMock(returncode=0, stderr="", stdout="")
            rendered = renderer.render_all([(1, "graph TD\n    A --> B")])

        assert len(rendered) == 1
        assert next(iter(rendered.values())) == (fake_png, "mermaid_1.png")
        assert run.call_count == 1

    def test_mermaid_render_passes_puppeteer_config(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """Container sandbox settings are forwarded to mmdc with -p."""
        config.puppeteer_config = "/tmp/puppeteer.json"
        renderer = MermaidRenderer(config, state, logger)

        with (
            patch("shutil.which", return_value="/usr/bin/mmdc"),
            patch("subprocess.run") as run,
            patch("pathlib.Path.is_file", return_value=True),
            patch("pathlib.Path.read_bytes", return_value=b"png"),
        ):
            run.return_value = MagicMock(returncode=0, stderr="", stdout="")
            renderer.render_all([(1, "graph TD\n    A --> B")])

        command = run.call_args.args[0]
        assert command[-2:] == ["-p", "/tmp/puppeteer.json"]

    def test_mermaid_render_requires_mmdc(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """A missing mmdc binary fails the CI build with installation guidance."""
        renderer = MermaidRenderer(config, state, logger)

        with (
            patch("shutil.which", return_value=None),
            pytest.raises(MermaidRenderError, match="mmdc not found"),
        ):
            renderer.render_all([(1, "graph TD\n    A --> B")])

    def test_mermaid_render_failure_is_strict(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """A Mermaid parse error fails instead of silently shipping source code."""
        renderer = MermaidRenderer(config, state, logger)

        with (
            patch("shutil.which", return_value="/usr/bin/mmdc"),
            patch("subprocess.run") as run,
            pytest.raises(MermaidRenderError, match="parse error"),
        ):
            run.return_value = MagicMock(returncode=1, stderr="parse error", stdout="")
            renderer.render_all([(1, "not valid Mermaid")])

    def test_mermaid_render_timeout_is_strict(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """A hung Chromium process fails the build after the fixed timeout."""
        renderer = MermaidRenderer(config, state, logger)

        with (
            patch("shutil.which", return_value="/usr/bin/mmdc"),
            patch(
                "subprocess.run",
                side_effect=subprocess.TimeoutExpired("mmdc", 60),
            ),
            pytest.raises(MermaidRenderError, match="timed out"),
        ):
            renderer.render_all([(1, "graph TD\n    A --> B")])

    def test_mermaid_render_deduplicates_identical_diagrams(
        self, config: EPUBConfig, state: BuildState, logger: logging.Logger
    ) -> None:
        """Repeated diagrams invoke mmdc once and reuse the cached image."""
        renderer = MermaidRenderer(config, state, logger)
        diagram = "graph TD\n    A --> B"

        with (
            patch("shutil.which", return_value="/usr/bin/mmdc"),
            patch("subprocess.run") as run,
            patch("pathlib.Path.is_file", return_value=True),
            patch("pathlib.Path.read_bytes", return_value=b"png"),
        ):
            run.return_value = MagicMock(returncode=0, stderr="", stdout="")
            rendered = renderer.render_all([(1, diagram), (2, diagram)])

        assert run.call_count == 1
        assert len(rendered) == 1

    def test_unrendered_mermaid_block_falls_back_to_source(
        self, state: BuildState, logger: logging.Logger
    ) -> None:
        """Unrendered Mermaid should remain readable instead of raising."""
        content = """# Diagram

```mermaid
graph TD
    A --> B
```
"""

        processed = process_mermaid_blocks(content, epub.EpubBook(), state, logger)

        assert "```mermaid" in processed
        assert "A --> B" in processed

    def test_embedded_mermaid_image_does_not_log_missing_file(
        self,
        tmp_path: Path,
        state: BuildState,
        logger: logging.Logger,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Mermaid EPUB assets should not be re-read from the source tree."""
        state.mermaid_added_to_book.add("mermaid_1.png")
        soup = BeautifulSoup(
            '<p><img alt="Diagram" src="images/mermaid_1.png"/></p>',
            "html.parser",
        )

        with caplog.at_level(logging.WARNING):
            embed_local_raster_images(
                soup,
                tmp_path / "README.md",
                tmp_path,
                epub.EpubBook(),
                state,
                logger,
            )

        assert "Local image not found" not in caplog.text
        assert soup.img is not None
        assert soup.img["src"] == "images/mermaid_1.png"


# =============================================================================
# Chapter Collection Tests
# =============================================================================


class TestChapterCollector:
    """Tests for ChapterCollector class."""

    def test_collect_single_file(self, tmp_path: Path, state: BuildState) -> None:
        """Test collecting a single markdown file."""
        readme = tmp_path / "README.md"
        readme.write_text("# Test")

        collector = ChapterCollector(tmp_path, state)
        chapters = collector.collect_all_chapters([("README.md", "Introduction")])

        assert len(chapters) == 1
        assert chapters[0].file_path == readme
        assert chapters[0].display_name == "Test"
        assert chapters[0].chapter_filename == "chap_01.xhtml"
        assert state.path_to_chapter["README.md"] == "chap_01.xhtml"

    def test_collect_folder(self, tmp_project: Path, state: BuildState) -> None:
        """Test collecting a folder with multiple files."""
        collector = ChapterCollector(tmp_project, state)
        chapters = collector.collect_all_chapters([("01-test-chapter", "Test Chapter")])

        assert len(chapters) == 2  # README.md and section.md
        assert chapters[0].is_folder_overview is True
        assert chapters[0].folder_name == "Chapter Overview"
        assert chapters[0].file_title == "概览"
        assert chapters[1].is_folder_overview is False

    def test_path_mapping(self, tmp_project: Path, state: BuildState) -> None:
        """Test that path mapping is built correctly."""
        collector = ChapterCollector(tmp_project, state)
        collector.collect_all_chapters(
            [
                ("README.md", "Introduction"),
                ("01-test-chapter", "Test Chapter"),
            ]
        )

        assert "README.md" in state.path_to_chapter
        assert "01-test-chapter" in state.path_to_chapter
        assert "01-test-chapter/README.md" in state.path_to_chapter


# =============================================================================
# HTML Generation Tests
# =============================================================================


class TestHTMLGeneration:
    """Tests for HTML generation."""

    def test_create_chapter_html_overview(self) -> None:
        """Test creating HTML for an overview chapter."""
        html = create_chapter_html(
            display_name="Introduction",
            file_title="Introduction",
            html_content="<h1>Introduction</h1><h2>Table of Contents</h2><p>Content</p>",
            is_overview=True,
        )

        assert "<!DOCTYPE html>" in html
        assert '<html xmlns="http://www.w3.org/1999/xhtml"' in html
        assert 'lang="zh"' in html
        assert html.count("<h1>Introduction</h1>") == 1
        assert "<h2>目录</h2>" in html
        assert "<p>Content</p>" in html

    def test_create_chapter_html_section(self) -> None:
        """Test creating HTML for a section chapter."""
        html = create_chapter_html(
            display_name="Chapter",
            file_title="Section",
            html_content="<h1>Section</h1><h2>Best Practices</h2><p>Content</p>",
            is_overview=False,
        )

        assert "<h2>Section</h2>" in html
        assert "<h1>Section</h1>" not in html
        assert "<h2>最佳实践</h2>" in html


class TestMarkdownPreprocessing:
    """Tests for markdown preprocessing helpers."""

    def test_prepare_root_readme_for_epub_replaces_hero_block(self) -> None:
        content = """<picture>old</picture>

[![Badge](https://example.com/badge.svg)](https://example.com)

# Claude Code 中文全面上手指南

导语内容

---

## 目录

正文内容
"""

        processed = prepare_root_readme_for_epub(content)

        assert "<picture>" not in processed
        assert "follow-qr.jpg" in processed
        assert "luongnv89/claude-howto" in processed
        assert processed.startswith("# Claude Code 中文全面上手指南")
        assert "导语内容" not in processed
        assert "## 目录" in processed

    def test_html_escaping(self) -> None:
        """Test that HTML special characters are escaped."""
        html = create_chapter_html(
            display_name="<script>alert('xss')</script>",
            file_title="Test & Title",
            html_content="<p>Content</p>",
            is_overview=True,
        )

        assert "&lt;script&gt;" in html
        # Note: Python's html.escape uses &#x27; for single quotes
        assert "<script>alert" not in html


# =============================================================================
# Chapter Order Tests
# =============================================================================


class TestChapterOrder:
    """Tests for chapter ordering."""

    def test_get_chapter_order(self) -> None:
        """Test that chapter order is defined correctly."""
        order = get_chapter_order()

        assert len(order) > 0
        assert order[0] == ("README.md", "首页")

        # Check that all expected chapters are present
        chapter_names = [name for name, _ in order]
        assert "01-slash-commands" in chapter_names
        assert "02-memory" in chapter_names
        assert "10-cli" in chapter_names
        assert "resources.md" in chapter_names


class TestMarkdownTitleExtraction:
    """Tests for extracting markdown H1 titles."""

    def test_extract_markdown_h1(self, tmp_path: Path) -> None:
        md = tmp_path / "sample.md"
        md.write_text("# 中文标题\n\n正文\n", encoding="utf-8")

        assert extract_markdown_h1(md) == "中文标题"

    def test_extract_markdown_h1_ignores_code_blocks(self, tmp_path: Path) -> None:
        md = tmp_path / "sample.md"
        md.write_text(
            "```md\n# fake\n```\n\n# Real Title\n",
            encoding="utf-8",
        )

        assert extract_markdown_h1(md) == "Real Title"


# =============================================================================
# Logging Tests
# =============================================================================


class TestLogging:
    """Tests for logging setup."""

    def test_setup_logging_default(self) -> None:
        """Test default logging setup."""
        logger = setup_logging(verbose=False)
        assert logger.name == "epub_builder"

    def test_setup_logging_verbose(self) -> None:
        """Test verbose logging setup."""
        logger = setup_logging(verbose=True)
        assert logger.name == "epub_builder"


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for the full build process."""

    def test_build_without_mermaid(
        self, tmp_project: Path, logger: logging.Logger
    ) -> None:
        """Test building an EPUB without Mermaid diagrams."""
        from build_epub import build_epub_async

        config = EPUBConfig(
            root_path=tmp_project,
            output_path=tmp_project / "test.epub",
        )

        # Override chapter order for minimal test
        with patch("build_epub.get_chapter_order") as mock_order:
            mock_order.return_value = [("README.md", "Introduction")]

            result = build_epub_async(config, logger)

            assert result.exists()
            assert result.suffix == ".epub"


# =============================================================================
# Run tests
# =============================================================================


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
