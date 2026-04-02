from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import cli


class _DummyCLI:
    _stream_in_code_fence = False


def test_render_assistant_response_uses_markdown_for_formatted_text():
    response = """**Files changed**\n- `cli.py`\n- *tests/test_cli_response_rendering.py*\n"""

    renderable = cli._render_assistant_response(response)

    console = Console(record=True, force_terminal=False, color_system=None, width=80)
    console.print(Panel(renderable))
    output = console.export_text()

    assert "Files changed" in output
    assert "cli.py" in output
    assert "tests/test_cli_response_rendering.py" in output
    assert "**Files changed**" not in output
    assert "`cli.py`" not in output


def test_render_assistant_response_preserves_ansi_text():
    ansi = "\x1b[31mred text\x1b[0m"

    renderable = cli._render_assistant_response(ansi)

    assert isinstance(renderable, Text)
    assert renderable.plain == "red text"


def test_format_streamed_response_line_restyles_basic_markdown():
    dummy = _DummyCLI()

    rendered = cli.HermesCLI._format_streamed_response_line(
        dummy,
        "**Files changed** · *important* · `cli.py`",
        "\033[38;2;255;248;220m",
    )

    assert "**Files changed**" not in rendered
    assert "*important*" not in rendered
    assert "`cli.py`" not in rendered
    assert "Files changed" in rendered
    assert "important" in rendered
    assert "cli.py" in rendered
    assert "\033[1m" in rendered
    assert "\033[3m" in rendered
    assert "\033[4m" in rendered
