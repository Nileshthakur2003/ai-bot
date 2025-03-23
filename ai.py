import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(user_message):
    """
    Sends a user message to the OpenAI API and returns the generated response.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a friendly community assistant. Reply to the user query: {user_message}",
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't generate a response. Please try again later."
