import click
from viscli.session_manager import SessionManager

@click.command("ask")
@click.option("--question", type=str, required=True, help="Question about the dataset.")
def ask_command(question):
    """
    Store the question in session and display it.
    """
    try:
        session = SessionManager()
        session.set("question", question)
        click.echo(f"Question: {question}")
    except Exception as e:
        click.echo(f"Error processing question: {e}")
