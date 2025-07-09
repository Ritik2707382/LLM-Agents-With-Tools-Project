# LLM Agent

This is an interactive AI agent powered by OpenAI's GPT models. The agent can process user input and determine whether to respond directly or invoke tools for specific tasks like fetching the current time and evaluating mathematical expressions.

## Features

- **Interactive chatbot interface**
- **Supports tools for:**
  - Fetching the current time in different time zones.
  - Evaluating mathematical expressions safely.
- **Memory system** to track past interactions.
- **Uses OpenAI's GPT-4o-mini** for decision-making.

## Technologies Used

- **Python**
- **OpenAI API**
- **ZoneInfo** (for time zones)
- **Regular Expressions** (for JSON parsing)
- **Math library** (for calculations)
- **dotenv** (for loading environment variables)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/llm-agent.git
   cd llm-agent
2. **Install dependencies:**
    ```sh
   pip install -r requirements.txt
3. **Set up your OpenAI API key:**
Create a `.env` file in the project directory.
Add the following line:
   ```sh
   OPENAI_API_KEY=your_openai_api_key_here


## Usage
**Run the agent:**
   ```bash
   python main.py ```
The agent will prompt you for input and respond accordingly. To exit, type exit, bye, or close.

## Tools

**⏰ Time Tool**
1. Fetches the current time for a given city timezone (e.g., Asia/Tokyo, America/New_York).
2. Returns the formatted current time.

**🧮 Calculator Tool**
1. Evaluates simple mathematical expressions.
2. Supports operations like addition, subtraction, multiplication, division, square root, and cube root
3. Ensures safe execution using restricted evaluation.


