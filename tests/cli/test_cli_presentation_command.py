from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from cli import HermesCLI


def _make_cli_stub():
    cli = HermesCLI.__new__(HermesCLI)
    cli.presentation_mode = "claude_code"
    cli._tui_style_base = {
        "prompt": "#fff",
        "input-area": "#fff",
        "input-rule": "#aaa",
        "prompt-working": "#888 italic",
    }
    cli._app = SimpleNamespace(style=None)
    cli._invalidate = MagicMock()
    cli.console = MagicMock()
    return cli


class TestCliPresentationCommand:
    def test_show_current_presentation_mode(self, capsys):
        cli = _make_cli_stub()

        cli._handle_presentation_command("/presentation")

        output = capsys.readouterr().out
        assert "Current presentation mode: claude_code" in output

    def test_switch_presentation_mode_persists_and_refreshes(self, capsys):
        cli = _make_cli_stub()

        with patch("cli.save_config_value", return_value=True):
            cli._handle_presentation_command("/presentation classic")

        output = capsys.readouterr().out
        assert "Presentation mode set to: classic (saved)" in output
        assert "TUI refreshed." in output
        assert cli.presentation_mode == "classic"
        cli._invalidate.assert_called_once_with(min_interval=0.0)

    def test_alias_ui_dispatches_via_process_command(self):
        cli = _make_cli_stub()
        with patch.object(cli, "_handle_presentation_command") as mock_handle:
            assert cli.process_command("/ui classic") is True
        mock_handle.assert_called_once_with("/ui classic")
