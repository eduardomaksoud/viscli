import os
import click
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from viscli.session_manager import SessionManager

@click.command("init-db")
@click.option("--docs-dir", type=click.Path(exists=True), required=True, help="Path to the directory containing best practice documents.")
def init_db_command(docs_dir):
    """
    Initialize the FAISS vector database with documents.
    """
    try:
        # Load documents
        documents = []
        for filename in os.listdir(docs_dir):
            file_path = os.path.join(docs_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    documents.append(f.read())

        # Initialize embeddings and FAISS
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(documents, embeddings)

        # Save FAISS database to disk
        db_path = "faiss_db"
        vector_store.save_local(db_path)

        # Store the FAISS path in the session
        session = SessionManager()
        session.set("faiss_db_path", db_path)

        click.echo(f"FAISS database initialized and saved to '{db_path}'.")

    except Exception as e:
        click.echo(f"Error initializing FAISS database: {e}")