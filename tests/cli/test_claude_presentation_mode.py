from cli import HermesCLI


def _make_cli(*, presentation_mode="claude_code"):
    cli_obj = HermesCLI.__new__(HermesCLI)
    cli_obj.presentation_mode = presentation_mode
    cli_obj.show_reasoning = False
    cli_obj._stream_box_opened = False
    cli_obj._stream_buf = ""
    cli_obj._stream_text_ansi = ""
    cli_obj._deferred_content = ""
    cli_obj._reasoning_box_opened = False
    cli_obj._stream_prefilt = ""
    cli_obj._in_reasoning_block = False
    cli_obj._close_reasoning_box = lambda: None
    return cli_obj


class TestClaudePresentationMode:
    def test_claude_mode_normalizes_streaming_behavior(self, monkeypatch):
        cli_obj = _make_cli(presentation_mode="claude_code")
        seen = []
        monkeypatch.setattr("cli._cprint", lambda text: seen.append(text))

        cli_obj._emit_stream_text("Hello\n")
        cli_obj._flush_stream()

        joined = "\n".join(seen)
        assert "╭─" not in joined
        assert "╰" not in joined

    def test_classic_mode_keeps_boxed_streaming_behavior(self, monkeypatch):
        cli_obj = _make_cli(presentation_mode="classic")
        seen = []
        monkeypatch.setattr("cli._cprint", lambda text: seen.append(text))

        cli_obj._emit_stream_text("Hello\n")
        cli_obj._flush_stream()

        joined = "\n".join(seen)
        assert "╭─" in joined
        assert "╰" in joined
