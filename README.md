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
