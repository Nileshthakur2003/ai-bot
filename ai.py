import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client using the API key
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

def get_ai_response(user_message):
    """
    Sends a user message to Cohere's Chat API and returns the response text.
    """
    try:
        # Query the Cohere Chat API
        response = co.chat(
            model="command-a-03-2025",  # Model name
            messages=[{"role": "user", "content": user_message}]
        )
        # Extract the AI-generated response
        return response.message.content[0].text.strip()
    except Exception as e:
        # Handle errors gracefully
        print(f"Error with Cohere Chat API: {e}")
        return "Sorry, I couldn't generate a response. Please try again later."
