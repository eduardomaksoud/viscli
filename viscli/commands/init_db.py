import os
import click
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from viscli.session_manager import SessionManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@click.command("init-db")
@click.option("--docs-dir", type=click.Path(exists=True), required=True, help="Path to the directory containing best practice documents.")
def init_db_command(docs_dir):
    """
    Initialize the FAISS vector database with documents.
    """
    try:
        # Validate directory and load documents
        if not os.path.isdir(docs_dir):
            raise ValueError("Provided path is not a directory.")

        documents = []
        for filename in os.listdir(docs_dir):
            file_path = os.path.join(docs_dir, filename)
            if os.path.isfile(file_path) and filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append(f.read())

        if not documents:
            raise ValueError("No valid .txt documents found in the provided directory.")

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it using `set_key`.")

        # Initialize embeddings and FAISS
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vector_store = FAISS.from_texts(documents, embeddings)

        # Save FAISS database to disk
        db_path = os.path.abspath("faiss_db")
        vector_store.save_local(db_path)

        # Store the FAISS path in the session
        session = SessionManager()
        session.set("faiss_db_path", db_path)

        click.echo(f"FAISS database initialized and saved to '{db_path}'.")

    except ValueError as ve:
        click.echo(f"Validation Error: {ve}")
    except Exception as e:
        click.echo(f"Error initializing FAISS database: {e}")
