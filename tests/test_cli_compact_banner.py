"""Smoke tests for the compact banner.

History: this file originally tested ccross2-local word-wrap behavior that
reflowed banner copy across multiple rows on narrow terminals (commit
5b325047). The 0.9 merge took upstream's skin-aware banner path instead,
which uses truncation + a dedicated `tiny_line` branch for sub-30-column
terminals. The word-wrap feature can be re-added as a follow-up, but the
old-shape assertions no longer describe the banner we ship.

These smoke tests replace the word-wrap assertions with shape-only checks
that hold under both the current (truncation) path and a hypothetical
future word-wrap path.
"""

import os
from unittest.mock import patch

import cli


def test_compact_banner_returns_something_on_narrow_terminal():
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((32, 24))):
        banner = cli._build_compact_banner()
    assert banner
    assert "\n" in banner


def test_compact_banner_has_framed_layout_on_normal_terminal():
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((80, 24))):
        banner = cli._build_compact_banner()
    # box-drawing characters around the banner indicate a framed layout
    assert "╔" in banner and "╚" in banner


def test_compact_banner_tiny_branch_under_30_cols():
    # The tiny branch skips the box frame and prints a single-line label.
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((28, 24))):
        banner = cli._build_compact_banner()
    assert "╔" not in banner and "╚" not in banner
    assert "Nous Research" in banner
