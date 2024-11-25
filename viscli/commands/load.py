import pandas as pd
import json
import click
from viscli.session_manager import SessionManager

@click.command("load")
@click.option("--file", type=click.Path(exists=True), required=True, help="Path to the dataset file.")
def load_command(file):
    """
    Load a dataset and display its summary.
    """
    try:
        df = pd.read_csv(file)
        summary = {
            "dataset_name": file,
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "description": "This dataset includes the following columns: " + ", ".join(df.columns)
        }

        session = SessionManager()
        session.set("dataset_summary", summary)
        click.echo(json.dumps(summary, indent=4))

    except Exception as e:
        click.echo(f"Error loading dataset: {e}")
