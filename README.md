LLM Agent

This is an interactive AI agent powered by OpenAI's GPT models. The agent can process user input and determine whether to respond directly or invoke tools for specific tasks like fetching the current time and evaluating mathematical expressions.

Features

Interactive chatbot interface.

Supports tools for:

Fetching the current time in different time zones.

Evaluating mathematical expressions safely.

Memory system to track past interactions.

Uses OpenAI's GPT-4o-mini for decision-making.

Technologies Used

Python

OpenAI API

ZoneInfo (for time zones)

Regular Expressions (for JSON parsing)

Math library (for calculations)

dotenv (for loading environment variables)

Installation

Clone the repository:

git clone https://github.com/your-username/llm-agent.git
cd llm-agent

Install dependencies:

pip install -r requirements.txt

Set up your OpenAI API key:

Create a .env file in the project directory.

Add the following line:

OPENAI_API_KEY=your_openai_api_key_here

Usage

Run the agent:

python main.py

The agent will prompt you for input and respond accordingly. To exit, type exit, bye, or close.

Tools

Time Tool

Fetches the current time for a given city timezone (e.g., Asia/Tokyo, America/New_York).

Returns the formatted current time.

Calculator Tool

Evaluates simple mathematical expressions.

Supports operations like addition, subtraction, multiplication, division, square root, cube root, and trigonometric functions.

Ensures safe execution using restricted evaluation.

Example Interactions

Checking time:

You: What time is it in Europe/London?
Agent: The current time is 2025-03-23 14:30:00 GMT+0000.

Mathematical calculation:
You: What is the square root of 64?
Agent: The result of 'sqrt(64)' is 8.
