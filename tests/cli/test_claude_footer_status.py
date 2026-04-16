from datetime import datetime, timedelta
from unittest.mock import patch

from cli import HermesCLI


def _make_cli(*, presentation_mode="claude_code"):
    cli_obj = HermesCLI.__new__(HermesCLI)
    cli_obj.presentation_mode = presentation_mode
    cli_obj.model = "anthropic/claude-opus-4.6"
    cli_obj.session_start = datetime.now() - timedelta(minutes=9, seconds=44)
    cli_obj.conversation_history = [{"role": "user", "content": "hi"}]
    cli_obj.agent = None
    cli_obj._background_tasks = {"bg-1": object()}
    cli_obj._approval_state = {"command": "rm -rf /tmp/x"}
    cli_obj._status_bar_visible = True
    cli_obj._model_picker_state = None
    return cli_obj


class TestClaudeFooterStatus:
    def test_claude_mode_status_bar_mentions_workspace_approval_and_shells(self):
        cli_obj = _make_cli()

        with patch.dict("os.environ", {"TERMINAL_CWD": "/home/cc/cDesign"}, clear=False):
            text = cli_obj._build_status_bar_text(width=140)

        assert "claude-opus-4.6" in text
        assert "cDesign" in text
        assert "approval" in text
        assert "1 shell" in text

    def test_claude_mode_status_bar_fragments_are_segmented(self):
        cli_obj = _make_cli()

        with patch.dict("os.environ", {"TERMINAL_CWD": "/home/cc/cDesign"}, clear=False):
            fragments = cli_obj._get_status_bar_fragments()

        assert len(fragments) > 3
        joined = "".join(text for _, text in fragments)
        assert "cDesign" in joined
        assert "approval" in joined
        assert "1 shell" in joined
        assert any(style == "class:status-bar-strong" for style, _ in fragments)

    def test_classic_mode_status_bar_does_not_force_new_footer_fields(self):
        cli_obj = _make_cli(presentation_mode="classic")

        with patch.dict("os.environ", {"TERMINAL_CWD": "/home/cc/cDesign"}, clear=False):
            text = cli_obj._build_status_bar_text(width=140)

        assert "approval" not in text
        assert "1 shell" not in text
