import pytest
from click.testing import CliRunner
from viscli.commands.run import run_command

def test_run_command(tmp_path):
    """Test the `run` command for executing scripts and saving visualizations."""
    runner = CliRunner()

    # Mock script directory with an example script
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    script_file = scripts_dir / "1_bar_chart.py"
    script_file.write_text("""
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'Date': ['2023-01-01', '2023-01-02'], 'Sales': [100, 200]})
plt.bar(df['Date'], df['Sales'])
plt.savefig('output.png')
""")

    # Directory for visualizations
    visualizations_dir = tmp_path / "visualizations"

    result = runner.invoke(run_command, ["--scripts-dir", str(scripts_dir), "--output-dir", str(visualizations_dir)])
    assert result.exit_code == 0

    # Verify the output image
    generated_image = visualizations_dir / "1_bar_chart.png"
    assert generated_image.exists()