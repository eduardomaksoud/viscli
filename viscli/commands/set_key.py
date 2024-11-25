import click
from dotenv import load_dotenv, set_key
import os

# Load environment variables
load_dotenv()

@click.command("set_key")
@click.option("--api-key", required=True, help="Set the OpenAI API key.")
def set_key_command(api_key):
    """
    Set the OpenAI API key in the .env file.
    """
    env_path = os.path.join(os.getcwd(), ".env")
    try:
        set_key(env_path, "OPENAI_API_KEY", api_key)
        click.echo("OpenAI API key has been set successfully.")
    except Exception as e:
        click.echo(f"Error setting API key: {e}")