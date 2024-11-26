import pytest
from click.testing import CliRunner
from viscli.commands.build import build_command
import json

def test_build_command(setup_env, session_manager, tmp_path, mock_openai_code_response):
    """
    Test the `build` command for generating Python scripts from suggestions.
    """
    runner = CliRunner()

    # Set up session data for dataset summary
    session_manager.set("dataset_summary", {"dataset_name": "data.csv", "columns": ["Date", "Sales"]})

    # Create a mock suggestions file
    suggestions_file = tmp_path / "suggestions.json"
    suggestions = [
        {
            "rank": 1,
            "type": "Bar Chart",
            "description": "Show sales trends",
            "notes": ["Ensure data is ordered in bar charts."]
        }
    ]
    with open(suggestions_file, "w") as f:
        json.dump(suggestions, f)

    # Directory to store generated scripts
    scripts_dir = tmp_path / "scripts"

    # Run the `build` command
    result = runner.invoke(build_command, ["--input", str(suggestions_file), "--dirpath", str(scripts_dir)])
    assert result.exit_code == 0  # Ensure the command executed successfully

    # Verify the generated script file
    script_file = scripts_dir / "1_bar_chart.py"
    assert script_file.exists()

    # Validate the content of the generated script
    with open(script_file, "r") as f:
        code = f.read()
    
    # Assert specific parts of the generated code
    assert "import matplotlib.pyplot as plt" in code
    assert "df = pd.read_csv('data.csv')" in code
    assert "plt.bar(df['Date'], df['Sales'])" in code
    assert "plt.savefig('output.png')" in code