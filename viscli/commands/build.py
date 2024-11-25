import os
import json
import click
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from viscli.session_manager import SessionManager

# Load environment variables
load_dotenv()

@click.command("build")
@click.option("--input", type=click.Path(exists=True), required=True, help="Path to the suggestions.json file.")
@click.option("--dirpath", type=click.Path(), required=True, help="Directory to save generated Python scripts.")
def build_command(input, dirpath):
    """
    Generate Python scripts for visualization suggestions using GPT.
    """
    try:
        # Ensure output directory exists
        os.makedirs(dirpath, exist_ok=True)

        # Load suggestions from file
        with open(input, "r") as f:
            suggestions = json.load(f)

        # Retrieve dataset summary from session
        session = SessionManager()
        dataset_summary = session.get("dataset_summary")
        if not dataset_summary:
            click.echo("Error: Dataset summary not found in the session. Use the `load` command first.")
            return

        dataset_name = dataset_summary["dataset_name"]

        # Validate OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            click.echo("Error: OpenAI API key not set. Use `set-key` to set it.")
            return

        # Initialize ChatOpenAI
        llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key, temperature=0)

        # Generate Python scripts for each suggestion
        for suggestion in suggestions:
            rank = suggestion["rank"]
            vis_type = suggestion["type"]
            description = suggestion["description"]
            notes = suggestion.get("notes", [])
            filename = f"{rank}_{vis_type.lower().replace(' ', '_')}.py"
            filepath = os.path.join(dirpath, filename)

            # Generate Python code using GPT
            raw_code = generate_code_with_llm(llm, vis_type, description, notes, dataset_name, dataset_summary)

            # Clean and format the generated code
            clean_code = clean_generated_code(raw_code)

            # Save script to file
            with open(filepath, "w") as script_file:
                script_file.write(clean_code)

            click.echo(f"Generated script: {filepath}")

    except Exception as e:
        click.echo(f"Error generating scripts: {e}")


def generate_code_with_llm(llm, vis_type, description, notes, dataset_name, metadata):
    """
    Use LLM (ChatOpenAI) to generate Python visualization code.
    """
    try:
        # Construct the system and user prompts
        notes_text = "\n".join(f"- {note}" for note in notes)
        system_prompt = (
            "You are an expert Python programmer specializing in data visualization. "
            "Your task is to generate Python scripts using Matplotlib or Seaborn to create visualizations. "
            "Each script must strictly adhere to the following rules:\n"
            "- Only include executable Python code surrounded by triple backticks (```python).\n"
            "- Do not include any text, explanations, or descriptions outside the code block.\n"
            "- The code should include necessary imports for Matplotlib or Seaborn.\n"
            f"- Load the dataset using pandas (assume it's named '{dataset_name}').\n"
            "- Use the following dataset metadata to customize the visualization:\n"
            f"{json.dumps(metadata, indent=4)}\n"
            "- Create the specified visualization as described.\n"
            "- Save the visualization as an image (e.g., 'output.png').\n"
            "- Add comments inline to explain the code (within the code block).\n"
            "- Ensure the code is properly formatted and executable.\n\n"
            "Example output format:\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "# Load your dataset\n"
            "df = pd.read_csv('your_dataset.csv')\n\n"
            "# Create the visualization\n"
            "plt.plot(df['x'], df['y'])\n"
            "plt.title('Your Title')\n"
            "plt.xlabel('X-axis Label')\n"
            "plt.ylabel('Y-axis Label')\n\n"
            "# Save the plot\n"
            "plt.savefig('output.png')\n"
            "```\n"
            "Do not include any additional text outside the code block."
        )

        user_prompt = (
            f"Dataset Name: {dataset_name}\n"
            f"Visualization Type: {vis_type}\n"
            f"Description: {description}\n"
            f"Visualization Best Practices:\n{notes_text}\n"
            f"Please provide the Python code."
        )

        # Generate response using ChatOpenAI
        response = llm.invoke(
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        return response.content.strip()

    except Exception as e:
        return f"# Error generating code: {e}\n"


def clean_generated_code(raw_code):
    """
    Extract, clean, and format Python code from raw LLM output.
    """
    try:
        # Match Python code block enclosed by ```python ... ```
        code_block = re.search(r"```python\s*(.*?)\s*```", raw_code, re.DOTALL)

        # If no match is found, return the raw code with a warning comment
        if not code_block:
            return f"# Warning: Code block not found. Review the LLM output.\n{raw_code.strip()}\n"

        # Extract the code block and clean up
        extracted_code = code_block.group(1).strip()

        # Remove unnecessary whitespace and ensure proper formatting
        cleaned_code = "\n".join(line for line in extracted_code.splitlines())

        # Add a final newline for consistency
        return cleaned_code + "\n"
    except Exception as e:
        return f"# Error cleaning code: {e}\n"
