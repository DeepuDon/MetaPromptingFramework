import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core import exceptions

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error configuring Google Generative AI: {e}")
    exit(1)

def execute_prompt(prompt:str, model_name:str="gemini-2.5-flash") -> str:
    """
    Executes a prompt provided by in the variable `prompt` using the specified model.

    Args:
        prompt (str): The prompt to be executed.
        model_name (str): The name of the model to use. Default is "gemini-2.5-flash".

    Returns:
        str: The response text from the model.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except exceptions.GoogleAPICallError as e:
        print(f"API call error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
if __name__ == "__main__":
    print("---- Running Prompt Executor Tests ----")

    # Test 1: Successful execution
    print("\n[Test 1: Valid Prompt]")
    test_prompt = "Explain the concept of a meta-prompt in one sentence."
    response = execute_prompt(test_prompt)
    if response:
        print(f"Prompt : {test_prompt}")
        print(f"Response : {response}")
    else:
        print("Failed to get a response from the model.")

    # Test 2: Handling a faulty prompt (empty string)
    print("\n[Test 2: Empty Prompt]")
    test_prompt_empty = ""
    response_empty = execute_prompt(test_prompt_empty)
    if response_empty:
        print(f"Prompt : {test_prompt_empty}")
        print(f"Response : {response_empty}")
    else:
        print("Handled empty prompt gracefully as expected.")

    print("---- End of Tests ----")