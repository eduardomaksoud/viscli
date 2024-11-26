import os
import pytest
from unittest.mock import patch
from viscli.session_manager import SessionManager

@pytest.fixture
def setup_env():
    """Fixture to set up the environment with a mock OpenAI API key."""
    os.environ["OPENAI_API_KEY"] = "test-key"
    yield
    del os.environ["OPENAI_API_KEY"]

@pytest.fixture
def session_manager():
    """Fixture to create and return a clean SessionManager instance."""
    session = SessionManager()
    session.set("faiss_db_path", "/path/to/mock_faiss_db")
    return session

@pytest.fixture
def mock_openai_suggest_response():
    """Mock the OpenAI GPT response for generating visualization suggestions."""
    with patch("langchain_openai.ChatOpenAI.invoke") as mock_invoke:
        mock_invoke.return_value = type(
            "MockResponse",
            (object,),
            {"content": '[{"rank": 1, "type": "Bar Chart", "description": "Show sales trends", "notes": []}]'}
        )
        yield mock_invoke

@pytest.fixture
def mock_openai_code_response():
    """
    Mock the OpenAI GPT response for generating Python code.
    """
    with patch("langchain_openai.ChatOpenAI.invoke") as mock_invoke:
        mock_invoke.return_value = type(
            "MockResponse",
            (),
            {
                "content": "```python\n"
                           "import matplotlib.pyplot as plt\n"
                           "import pandas as pd\n"
                           "df = pd.read_csv('data.csv')\n"
                           "plt.bar(df['Date'], df['Sales'])\n"
                           "plt.savefig('output.png')\n"
                           "```"
            }
        )
        yield mock_invoke


@pytest.fixture
def mock_faiss_search(tmp_path):
    """Fixture to mock FAISS vectorstore and its methods."""
    # Create a mock FAISS database path
    mock_db_path = tmp_path / "mock_faiss_db"
    mock_db_path.mkdir(parents=True, exist_ok=True)

    # Patch FAISS.load_local and FAISS.similarity_search
    with patch("langchain_community.vectorstores.FAISS.load_local") as mock_load_local, \
         patch("langchain_community.vectorstores.FAISS.similarity_search") as mock_search:
        mock_load_local.return_value = type(
            "MockFAISS",
            (),
            {"similarity_search": lambda query, k: [
                type("MockResult", (), {"page_content": "Ensure data is ordered in bar charts."}),
                type("MockResult", (), {"page_content": "Use contrasting colors for better readability."}),
            ]}
        )
        mock_search.return_value = [
            type("MockResult", (), {"page_content": "Ensure data is ordered in bar charts."}),
            type("MockResult", (), {"page_content": "Use contrasting colors for better readability."}),
        ]
        yield mock_search


