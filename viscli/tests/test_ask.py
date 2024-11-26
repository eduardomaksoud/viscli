from click.testing import CliRunner
from viscli.commands.ask import ask_command

def test_ask_command(session_manager):
    """Test the `ask` command for saving a question."""
    runner = CliRunner()

    result = runner.invoke(ask_command, ["--question", "Quais são as tendências de vendas?"])
    assert result.exit_code == 0
    assert "Question" in result.output
    assert session_manager.get("question") == "Quais são as tendências de vendas?"
