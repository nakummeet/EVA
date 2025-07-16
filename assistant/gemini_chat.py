# assistant/commands/gemini_handler.py

from google import genai
from config import GEMINI_API_KEY

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
#chat_session = client.start_chat(history=[])


def handle_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Extract the generated text safely
        reply = response.text.strip() if hasattr(response, "text") else str(response)
        return reply
    except Exception as e:
        print("⚠️ Gemini API error:", e)
        return "Sorry, I couldn't generate a response right now."
