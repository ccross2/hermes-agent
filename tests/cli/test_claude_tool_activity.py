from cli import HermesCLI


def _make_cli(*, presentation_mode="claude_code", tool_progress_mode="new"):
    cli_obj = HermesCLI.__new__(HermesCLI)
    cli_obj.presentation_mode = presentation_mode
    cli_obj.tool_progress_mode = tool_progress_mode
    cli_obj._spinner_text = ""
    cli_obj._status_message = ""
    cli_obj._invalidate = lambda *args, **kwargs: None
    cli_obj._voice_mode = False
    return cli_obj


class TestClaudeToolActivity:
    def test_claude_mode_tool_start_uses_flat_activity_summary(self):
        cli_obj = _make_cli(presentation_mode="claude_code")

        cli_obj._on_tool_progress(
            "tool.started",
            function_name="terminal",
            preview="find moonshine in nix store",
        )

        assert cli_obj._spinner_text == "Bash · find moonshine in nix store"

    def test_classic_mode_tool_start_keeps_legacy_spinner_format(self):
        cli_obj = _make_cli(presentation_mode="classic")

        cli_obj._on_tool_progress(
            "tool.started",
            function_name="terminal",
            preview="find moonshine in nix store",
        )

        assert "·" not in cli_obj._spinner_text
        assert "find moonshine in nix store" in cli_obj._spinner_text
