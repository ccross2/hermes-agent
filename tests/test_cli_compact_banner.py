import os
from unittest.mock import patch

import cli


def test_compact_banner_reflows_instead_of_truncating_words():
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((32, 24))):
        banner = cli._build_compact_banner()

    assert "AI Agent Framework" in banner
    assert "Messenger of the Digital" in banner
    assert "Gods" in banner
    assert "Nous Research" in banner
    assert "AI Agent F[/]" not in banner
    assert "Digital G[/]" not in banner


def test_compact_banner_keeps_two_line_layout_when_there_is_room():
    with patch("shutil.get_terminal_size", return_value=os.terminal_size((60, 24))):
        banner = cli._build_compact_banner()

    assert "⚕ NOUS HERMES - AI Agent Framework" in banner
    assert "Messenger of the Digital Gods  ·  Nous Research" in banner
