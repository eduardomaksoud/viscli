from click.testing import CliRunner
from viscli.commands.load import load_command

def test_load_command(tmp_path, session_manager):
    """Test the `load` command for loading a dataset."""
    runner = CliRunner()

    # Create a mock CSV file
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("Date,Sales\n2023-01-01,100\n2023-01-02,200")

    result = runner.invoke(load_command, ["--file", str(csv_file)])
    assert result.exit_code == 0
    assert "dataset_name" in result.output
    assert session_manager.get("dataset_summary")["dataset_name"] == str(csv_file)
