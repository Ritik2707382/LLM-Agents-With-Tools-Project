import datetime
from zoneinfo import ZoneInfo
from abc import ABC, abstractmethod
import math
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Initialize OpenAI API
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client_openai = OpenAI(api_key=openai_key)


# Define an Abstract base class tool that serves as a blueprint for other tools
class Tool(ABC):
    @abstractmethod  # This decorator ensures that subclasses must implement this method
    def name(self) -> str:
        pass  # Placeholder for method implementation in subclasses

    @abstractmethod
    def description(self) -> str:
        pass  # Placeholder for method implementation in subclasses

    @abstractmethod
    def use(self, *args, **kwargs):
        pass  # Placeholder for method implementation in subclasses


# Define a class Time Tool that extends the abstract Tool class
class TimeTool(Tool):
    def name(self):
        return "Time Tool"  # Returns the name of Tool

    def description(self):
        # Returns the description of tool
        return (
            """Gives the current time for a given city' timezone like Europe/Lisbon, America/New_York etc. If no
            timezone is provided, it returns the local time.""")

    def use(self, *args, **kwargs):
        format_type = "%Y-%m-%d %H:%M:%S %Z%z"  # Define the date-time format
        current_time = datetime.datetime.now()  # Fetches the current local time
        input_timezone = args[0] if args else None  # Retrieves the timezone argument if provided
        if input_timezone:
            try:  # Convert the time to given timezone
                current_time = current_time.astimezone(ZoneInfo(input_timezone))
            except Exception:
                # Return an error message for invalid timezone
                return f"Invalid timezone: {input_timezone}"
        # Returns the formatted current time
        return f"The current time is {current_time.strftime(format_type)}."


# Define a class Calculator Tool that extends the abstract tool class
class CalculatorTool(Tool):
    def name(self):
        return "Calculator Tool"  # Returns the name of tool

    def description(self):
        # Returns the description of tool
        return ("Evaluates simple mathematical expressions. Supports addition,"
                "subtraction, multiplication, division, square root, and cube root.")

    def use(self, *args, **kwargs):
        expression = args[0]  # Returns the mathematical expression from arguments
        try:
            # Evaluate the expression using a safe method
            result = self.safe_eval(expression)
            # Returns the result
            return f"The result of '{expression}' is {result} "
        except Exception as e:
            # Returns the error message
            return f"Sorry, I couldn't evaluate the expression '{expression}'. Error: {str(e)}"

    def safe_eval(self, expression):
        # Define a dictionary for allowed functions and constants for safe evaluation
        allowed_names = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'pow': pow,
            'sqrt': math.sqrt,
            'cbrt': lambda x: x ** (1 / 3),  # Cube root function
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }
        # Define the allowed characters in expression
        allowed_chars = "0123456789+-*/()., sqrt cbrt "

        # Ensures that the expression only contains allowed characters
        if any(char not in allowed_chars for char in expression):  # Check if any character is not in the allowed list
            raise ValueError("Invalid characters in expression.")  # Raise an error if invalid characters are found

        code = compile(expression, "<string>", "eval")  # Compile the expression into bytecode for evaluation

        # Ensures that only allowed function names are used in the expression
        for name in code.co_names:  # Iterate over the names detected in the compiled code
            if name not in allowed_names:  # Check if the name is not in the list of allowed names
                raise ValueError(f"Use of '{name}' is not allowed.")  # Raise an error if an unauthorized name is used

        return eval(code, {"__builtins__": None},
                    allowed_names)  # Evaluates the expression safely with restricted built-in functions


class Agent:
    def __init__(self):
        self.tools = []  # List to store available tools
        self.memory = []  # List to store results of previous interactions
        self.max_memory = 10  # Maximum number of memory entries allowed

    def add_tool(self, tool: Tool):
        # Add a tool to the agents list of tools
        self.tools.append(tool)

    def json_parser(self, input_string):
        # Extracts and parse a JSON object from a given string
        try:
            # Define regex patterns to match JSON objects from a given string
            code_block_pattern = r"```json\s*(\{.*?\})\s*```"
            # Search for JSON object within the block
            match = re.search(code_block_pattern, input_string, re.DOTALL)
            if match:
                json_str = match.group(1)  # Extracts the JSON string if found inside triple backticks
            else:
                # If no code block, try to match any JSON object in the string
                json_object_pattern = r"(\{.*?\})"  # Pattern to match any JSON object
                match = re.search(json_object_pattern, input_string, re.DOTALL)  # Search for JSON within text
                if match:
                    json_str = match.group(1)  # Extract JSON string if found
                else:
                    # Raise an error if no json object is found
                    raise ValueError("No JSON object found in the LLM response.")
            # Parse the JSON string into a dictionary
            json_dict = json.loads(json_str)  # Convert the JSON string to a Python dictionary
            if isinstance(json_dict, dict):  # Ensures that parsed object is dictionary
                return json_dict  # Returns the parsed JSON dictionary
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")  # Return the error message if JSON parsing fails
        print(f"LLM response was: {input_string}")  # Parse the original input string for debugging
        raise ValueError("Invalid JSON response from LLM.")  # Returns an error if JSON parsing fails

    def process_input(self, user_input):
        """
         Processes user input and determines whether to respond directly or use a tool
        """
        self.memory.append(f"User: {user_input}")  # Stores user input in memory
        self.memory = self.memory[-self.max_memory:]  # Keep memory within the max limit

        # Prepare conversation context
        context = "\n".join(self.memory)  # Combine past interactions into context
        # Prepare tool descriptions
        tool_descriptions = "\n".join(
            [f"- {tool.name()}: {tool.description()}" for tool in self.tools]
        )

        # Construct the prompt for LLM
        prompt = f"""
                You are an assistant that helps process user requests by determining the appropriate action and arguments based on the user's input.
                Context:
                {context}

                Available tools:
                {tool_descriptions}

                Instructions:
                - Decide whether to use a tool or respond directly to the user.
                - If you choose to use a tool, output a JSON object with "action" and "args" fields.
                - If you choose to respond directly, set "action": "respond_to_user" and provide your response in "args".
                - **Important**: Provide the response **only** as a valid JSON object. Do not include any additional text or formatting.
                - Ensure that the JSON is properly formatted without any syntax errors.

                Response Format:
                json
                {{"action": "<action_name>", "args": "<arguments>"}}

                Example Responses:
                - Using a tool: {{"action": "Time Tool", "args": "Asia/Tokyo"}}
                - Responding directly: {{"action": "respond_to_user", "args": "I'm here to help!"}}

                User Input: "{user_input}"
                """

        # Query the language model into the constructed prompt
        response = self.query_llm(prompt)
        # Store the response in memory
        self.memory.append(f"Agent: {response}")

        # Parse the response into a dictionary
        response_dict = self.json_parser(response)

        # Determine if the response is a direct message or a tool invocation
        if response_dict["action"] == "respond_to_user":
            return response_dict["args"]  # Return the direct response to the user
        else:
            # Find and use the appropriate tool
            for tool in self.tools:
                if tool.name().lower() == response_dict["action"].lower():  # Match tool by name
                    args = response_dict["args"]  # Extract arguments
                    if not isinstance(args, list):  # Ensure arguments are in list format
                        args = [args]
                    tool_result = tool.use(*args)  # Execute the tool with the provided arguments
                    return json.dumps(
                        {"action": response_dict["action"], "args": tool_result})  # Return the tool result as JSON

        return "I'm sorry, I couldn't process your request."  # Default response if no tool matches

    def query_llm(self, prompt):
        try:
            response = client_openai.chat.completions.create(
                model="gpt-4o-mini",  # Specify which model to be used
                messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}  # For formatting response in JSON
            )
            # Return the processed content, stripped of whitespace
            return response.choices[0].message.content.strip()
        # Return the error if it occurs during processing
        except Exception as e:
            return f"An error occurred: {e}"

    # Define the 'run' method within the class
    def run(self):
        # Print a greeting message when the agent starts
        print("LLM Agent: Hello! How can I assist you today?")

        # Start an infinite loop to keep the agent running
        while True:
            # Prompt the user for input and strip any leading/trailing whitespace
            user_input = input("You: ").strip()

            # Check if the user wants to exit the conversation
            if user_input.lower() in ["exit", "bye", "close"]:
                # Print a farewell message and break the loop to stop the agent
                print("Agent: See you later!")
                break

            # Process the user's input and generate a response
            response = self.process_input(user_input)

            # Print the agent's response
            print(f"Agent: {response}")


# Check if the script is being run directly
if __name__ == "__main__":
    # Create an instance of the 'Agent' class
    agent = Agent()

    # Add a tool for handling time-related tasks
    agent.add_tool(TimeTool())

    # Add a tool for handling mathematical calculations
    agent.add_tool(CalculatorTool())

    # Run the agent
    agent.run()
