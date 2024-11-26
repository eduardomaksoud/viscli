import os
from pathlib import Path
from click.testing import CliRunner
from viscli.commands.set_key import set_key_command
from dotenv import dotenv_values

def test_set_key_command(tmp_path):
    """Test the `set_key` command for setting the OpenAI API key."""
    runner = CliRunner()

    # Create a temporary .env file
    env_path = tmp_path / ".env"
    os.environ["DOTENV_PATH"] = str(env_path)  # Point to the temporary .env file

    # Test setting a valid API key
    result = runner.invoke(set_key_command, ["--api-key", "test-key"])
    assert result.exit_code == 0, f"Set-key failed: {result.output}"
    assert "OpenAI API key has been set successfully." in result.output

    # Verify the API key is saved in the temporary .env file
    env_values = dotenv_values(env_path)
    assert env_values.get("OPENAI_API_KEY") == "test-key"

    # Clean up
    os.environ.pop("DOTENV_PATH", None)
