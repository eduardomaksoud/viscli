import click
from viscli.commands.set_key import set_key_command
from viscli.commands.load import load_command
from viscli.commands.ask import ask_command
from viscli.commands.suggest import suggest_command
from viscli.commands.build import build_command
from viscli.commands.run import run_command
from viscli.commands.init_db import init_db_command
from viscli.commands.search_db import search_db_command

@click.group()
def main():
    """VisCLI: A tool for generating visualizations with GPT and RAG."""
    pass

# Register commands
main.add_command(set_key_command)
main.add_command(load_command)
main.add_command(ask_command)
main.add_command(suggest_command)
main.add_command(build_command)
main.add_command(run_command)
main.add_command(init_db_command)
main.add_command(search_db_command)

if __name__ == "__main__":
    main()
