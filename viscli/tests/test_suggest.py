import json
from click.testing import CliRunner
from viscli.commands.suggest import suggest_command

def test_suggest_command(
    setup_env,
    session_manager,
    mock_openai_suggest_response,
    mock_faiss_search,
    tmp_path
):
    """Test the `suggest` command for generating visualization suggestions."""
    runner = CliRunner()

    # Set up session data
    session_manager.set("question", "What are the sales trends?")
    session_manager.set(
        "dataset_summary",
        {"dataset_name": "data.csv", "columns": ["Date", "Sales"]}
    )
    session_manager.set("faiss_db_path", str(tmp_path / "mock_faiss_db"))

    # Output file for suggestions
    suggestions_file = tmp_path / "suggestions.json"

    # Run the `suggest` command
    result = runner.invoke(suggest_command, ["--output", str(suggestions_file)])
    assert result.exit_code == 0, f"Suggest command failed: {result.output}"

    # Verify that the suggestions file was created
    assert suggestions_file.exists(), "Suggestions file was not created"

    # Load and validate the contents of the suggestions file
    with suggestions_file.open() as f:
        suggestions = json.load(f)
       
