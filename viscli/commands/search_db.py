import click
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

@click.command("search-db")
@click.option("--query", required=True, help="Search query for visualization best practices.")
def search_db_command(query):
    """
    Search the FAISS vector database for relevant best practices.
    """
    try:
        # Load FAISS index
        vector_store = FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

        # Perform the search
        results = vector_store.similarity_search(query, k=3)
        click.echo("Search Results:")
        for result in results:
            click.echo(f"- {result.page_content}")
    except Exception as e:
        click.echo(f"Error querying FAISS database: {e}")
