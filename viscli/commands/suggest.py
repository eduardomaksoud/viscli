import click
import os
import json
import re
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from viscli.session_manager import SessionManager

@click.command("suggest")
@click.option("--output", type=click.Path(), required=True, help="Output file for visualization suggestions.")
def suggest_command(output):
    """
    Generate ranked visualization suggestions with enriched notes from RAG.
    """
    try:
        # Retrieve data from session
        session = SessionManager()
        question = session.get("question")
        dataset_summary = session.get("dataset_summary")
        faiss_db_path = session.get("faiss_db_path")

        if not question or not dataset_summary:
            click.echo("Error: Question or dataset summary not found. Use `ask` and `load` first.")
            return

        if not faiss_db_path or not os.path.exists(faiss_db_path):
            click.echo("Error: FAISS database not found or not initialized. Use `init-db` first.")
            return

        click.echo("Warning: Dangerous deserialization enabled for FAISS. Ensure the database is from a trusted source.")

        # Load FAISS from disk with deserialization allowed
        vector_store = FAISS.load_local(faiss_db_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

        # Validate OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            click.echo("Error: OpenAI API key not set. Use `set-key` to set it.")
            return

        # Initialize ChatOpenAI
        llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key, temperature=0)

        # Construct system and user prompts
        system_prompt = (
            "You are an expert in data visualization. Based on a dataset description "
            "and a user's question, generate a ranked JSON list of visualization suggestions. "
            "Each suggestion should include:\n\n"
            "[\n"
            "    {\n"
            "        \"rank\": <integer>,\n"
            "        \"type\": <string>,\n"
            "        \"description\": <string>,\n"
            "        \"notes\": []\n"
            "    },\n"
            "    ...\n"
            "]\n\n"
            "Do not include any extra text or explanations in your response. Only provide the JSON output."
        )
        user_prompt = (
            f"Dataset Description:\n{json.dumps(dataset_summary, indent=4)}\n\n"
            f"User's Question:\n{question}"
        )

        # Call LLM
        response = llm.invoke(
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        # Capture and clean LLM output
        raw_output = response.content.strip()
        match = re.search(r"\[.*\]", raw_output, re.DOTALL)
        if not match:
            raise ValueError("LLM response does not contain valid JSON.")
        suggestions = json.loads(match.group(0))

        # Enrich suggestions with RAG
        for suggestion in suggestions:
            query = f"Best practices for {suggestion['type']} visualization"
            results = vector_store.similarity_search(query, k=3)
            suggestion["notes"] = [result.page_content for result in results]

        # Save suggestions
        with open(output, "w") as f:
            json.dump(suggestions, f, indent=4)

        click.echo(f"Suggestions saved to {output}")

    except Exception as e:
        click.echo(f"Error generating suggestions: {e}")