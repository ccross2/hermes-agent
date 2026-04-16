from types import SimpleNamespace
from unittest.mock import patch

from cli import HermesCLI


def _make_cli(*, presentation_mode="claude_code"):
    cli_obj = HermesCLI.__new__(HermesCLI)
    cli_obj.presentation_mode = presentation_mode
    cli_obj.show_reasoning = False
    cli_obj._reasoning_box_opened = False
    cli_obj._deferred_content = ""
    cli_obj._stream_box_opened = False
    cli_obj._stream_buf = ""
    cli_obj._stream_text_ansi = ""
    cli_obj._close_reasoning_box = lambda: None
    return cli_obj


class TestClaudePresentationMode:
    @patch("cli._cprint")
    @patch("cli.shutil.get_terminal_size", return_value=SimpleNamespace(columns=80))
    def test_claude_mode_streaming_does_not_draw_response_box(self, _mock_term, mock_cprint):
        cli_obj = _make_cli(presentation_mode="claude_code")

        cli_obj._emit_stream_text("Hello world\n")
        cli_obj._flush_stream()

        rendered = "\n".join(call.args[0] for call in mock_cprint.call_args_list)
        assert "╭─" not in rendered
        assert "╰" not in rendered
        assert "Hello world" in rendered

    @patch("cli._cprint")
    @patch("cli.shutil.get_terminal_size", return_value=SimpleNamespace(columns=80))
    def test_classic_mode_streaming_still_draws_response_box(self, _mock_term, mock_cprint):
        cli_obj = _make_cli(presentation_mode="classic")

        cli_obj._emit_stream_text("Hello world\n")
        cli_obj._flush_stream()

        rendered = "\n".join(call.args[0] for call in mock_cprint.call_args_list)
        assert "╭─" in rendered
        assert "╰" in rendered
