import os
import re
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv



# Define custom tool using @tool decorator
@tool
def get_text_statistics(text: str, count_spaces: bool = True, count_punctuation: bool = True) -> dict:
    """
    An advanced text analysis tool that calculates various statistics.

    Parameters:
    - text (str): The input sentence or word.
    - count_spaces (bool): Whether to include spaces in the character count (default: True).
    - count_punctuation (bool): Whether to include punctuation in the character count (default: True).

    Returns:
    - dict: A dictionary with character count, word count, and more.
    """

    # Clean the text: remove leading/trailing spaces & extra surrounding quotes
    cleaned_text = text.strip().strip("'\"")

    # Remove punctuation if count_punctuation is False
    if not count_punctuation:
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation

    # Compute character count
    character_count = len(cleaned_text) if count_spaces else len(cleaned_text.replace(" ", ""))

    # Compute word count
    words = cleaned_text.split()
    word_count = len(words)

    # Compute average word length (avoid division by zero)
    avg_word_length = round(character_count / word_count, 2) if word_count > 0 else 0

    # Compute unique character count (excluding spaces)
    unique_chars = set(cleaned_text.replace(" ", ""))

    # Return detailed statistics as a dictionary
    return {
        "original_text": text,
        "cleaned_text": cleaned_text,
        "character_count": character_count,
        "word_count": word_count,
        "average_word_length": avg_word_length,
        "unique_character_count": len(unique_chars),
        "count_spaces": count_spaces,
        "count_punctuation": count_punctuation
    }


# Initialize DuckDuckGoSearch Tool
search = DuckDuckGoSearchResults()
tools = [search, get_text_statistics]

# Initialize the OpenAI Chat Model
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,  # Lower temperature makes responses more predictable
    model="gpt-4o-mini"
)

# Create the Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # Use OpenAI functions to decide when to invoke tools,
    verbose=True,
    handle_parsing_errors=True
)

# Test the Agent
if __name__ == "__main__":
    # Simple Search
    print(agent.run("What's the latest news about AI advancements?"))
    print(agent.run("What is length of this sentence 'Hello World' could be?"))
