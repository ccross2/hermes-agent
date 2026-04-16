from unittest.mock import MagicMock

from cli import HermesCLI


def _make_cli(*, presentation_mode="claude_code"):
    cli_obj = HermesCLI.__new__(HermesCLI)
    cli_obj.presentation_mode = presentation_mode
    cli_obj._spinner_text = ""
    cli_obj._tool_start_time = 0.0
    cli_obj._pending_tool_info = {}
    cli_obj._last_scrollback_tool = None
    cli_obj._voice_mode = False
    cli_obj._invalidate = MagicMock()
    return cli_obj


class TestClaudeToolActivity:
    def test_claude_mode_tool_start_uses_compact_activity_summary(self):
        cli_obj = _make_cli(presentation_mode="claude_code")

        cli_obj._on_tool_progress(
            "tool.started",
            function_name="terminal",
            preview="find moonshine in nix store",
        )

        assert cli_obj._spinner_text == "Bash · find moonshine in nix store"

    def test_claude_mode_activity_fragments_expose_live_lane(self):
        cli_obj = _make_cli(presentation_mode="claude_code")
        cli_obj._agent_running = True
        cli_obj._command_running = False

        cli_obj._on_tool_progress(
            "tool.started",
            function_name="terminal",
            preview="find moonshine in nix store",
        )

        fragments = cli_obj._get_activity_fragments()
        joined = "".join(text for _, text in fragments)

        assert "Bash" in joined
        assert "find moonshine in nix store" in joined
        assert "│" not in joined

    def test_classic_mode_tool_start_keeps_legacy_spinner_format(self):
        cli_obj = _make_cli(presentation_mode="classic")

        cli_obj._on_tool_progress(
            "tool.started",
            function_name="terminal",
            preview="find moonshine in nix store",
        )

        assert cli_obj._spinner_text
        assert "find moonshine in nix store" in cli_obj._spinner_text
