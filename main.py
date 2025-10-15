import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

def main():
    print("Hello from metapromptingframework!")

def execute_prompt(prompt):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")

    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    execute_prompt("Hello")
