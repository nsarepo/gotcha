import google.generativeai as genai
from config import GENAI_API_KEY

def get_emotional_support(user_input):
    """Interact with Gemini AI chatbot for emotional support."""
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(user_input)
        return response.text if response else "Sorry, I couldn't process your request."
    except Exception as e:
        return f"Error: {str(e)}"
